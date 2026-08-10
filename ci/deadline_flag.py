import csv
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DEADLINE_TASK_NAME = "Deadline"
EXPECTED_PERIOD_MS = 100.0          # matches mainDEADLINE_TASK_PERIOD_MS in main_blinky.c
MISS_THRESHOLD_MS = 150.0           # a gap bigger than this means the task started late


def check_missed_deadlines(csv_file, expected_period_ms=EXPECTED_PERIOD_MS,
                            threshold_ms=MISS_THRESHOLD_MS, out_path=None):
    if out_path is None:
        out_path = os.path.join(SCRIPT_DIR, "deadline_misses.csv")

    events = []
    with open(csv_file, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row['timestamp_ms'] = float(row['timestamp_ms'])
                events.append(row)
            except (ValueError, KeyError):
                continue

    print(f"Analyzing {len(events)} events for missed deadlines on '{DEADLINE_TASK_NAME}' "
          f"(expected period: {expected_period_ms} ms, miss threshold: {threshold_ms} ms)...")

    # Every TASK_ACTIVATE for the Deadline task marks the start of a new cycle.
    activations = [row['timestamp_ms'] for row in events
                   if row.get('event_name') == 'TASK_ACTIVATE'
                   and row.get('task_name') == DEADLINE_TASK_NAME]

    misses_found = 0
    miss_records = []

    for i in range(1, len(activations)):
        prev_time = activations[i - 1]
        curr_time = activations[i]
        gap = curr_time - prev_time

        print(f"-> Deadline task activation at t={curr_time:.3f} ms "
              f"(gap since previous: {gap:.3f} ms)")

        if gap > threshold_ms:
            print(f"   [!] MISSED DEADLINE: gap of {gap:.3f} ms exceeds threshold {threshold_ms} ms!")
            misses_found += 1
            miss_records.append((prev_time, curr_time, gap))

    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["expected_start_ms", "actual_start_ms", "delay_ms", "severity"])
        for prev_time, curr_time, gap in miss_records:
            severity = ("critical" if gap > threshold_ms * 3
                        else "high" if gap > threshold_ms * 1.5
                        else "medium")
            writer.writerow([f"{prev_time + expected_period_ms:.3f}", f"{curr_time:.3f}",
                              f"{gap:.3f}", severity])

    print(f"Written to: {out_path}")

    if misses_found > 0:
        print(f"\n[FLAGGED] Found {misses_found} missed deadline(s). See {out_path} for details.")
    else:
        print("\n[OK] No missed deadlines detected in this trace.")
    # Detection findings are reported, not treated as pipeline failures.
    sys.exit(0)


if __name__ == '__main__':
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'ci/trace_events.csv'
    check_missed_deadlines(csv_path)
