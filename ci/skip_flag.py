import csv
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

SKIPPED_TASK_NAME = "Skipped"
SKIP_THRESHOLD_MS = 10.0   # dispatch delay above this counts as "got skipped"


def check_skipped_task(csv_file, threshold_ms=SKIP_THRESHOLD_MS, out_path=None):
    if out_path is None:
        out_path = os.path.join(SCRIPT_DIR, "skip_flags.csv")

    events = []
    with open(csv_file, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row['timestamp_ms'] = float(row['timestamp_ms'])
                events.append(row)
            except (ValueError, KeyError):
                continue

    print(f"Analyzing {len(events)} events for skipped dispatches on '{SKIPPED_TASK_NAME}' "
          f"(threshold: {threshold_ms} ms dispatch delay)...")

    # Walk events in order, pairing each TASK_READY for the target task with
    # the next TASK_ACTIVATE for that same task.
    pending_ready_time = None
    skips_found = 0
    skip_records = []

    for row in events:
        if row.get('task_name') != SKIPPED_TASK_NAME:
            continue

        ev = row.get('event_name')
        t = row['timestamp_ms']

        if ev == 'TASK_READY':
            pending_ready_time = t
        elif ev == 'TASK_ACTIVATE' and pending_ready_time is not None:
            delay = t - pending_ready_time
            print(f"-> Ready at t={pending_ready_time:.3f} ms, ran at t={t:.3f} ms "
                  f"(dispatch delay: {delay:.3f} ms)")

            if delay > threshold_ms:
                print(f"   [!] SKIPPED: waited {delay:.3f} ms before running "
                      f"(threshold {threshold_ms} ms)!")
                skips_found += 1
                skip_records.append((pending_ready_time, t, delay))

            pending_ready_time = None

    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ready_time_ms", "activate_time_ms", "delay_ms", "severity"])
        for ready_t, act_t, delay in skip_records:
            severity = ("critical" if delay > threshold_ms * 5
                        else "high" if delay > threshold_ms * 3
                        else "medium")
            writer.writerow([f"{ready_t:.3f}", f"{act_t:.3f}", f"{delay:.3f}", severity])

    print(f"Written to: {out_path}")

    if skips_found > 0:
        print(f"\n[FLAGGED] Found {skips_found} skipped dispatch(es) for '{SKIPPED_TASK_NAME}'. "
              f"See {out_path} for details.")
    else:
        print(f"\n[OK] '{SKIPPED_TASK_NAME}' was never noticeably delayed in this trace.")
    # Detection findings are reported, not treated as pipeline failures.
    sys.exit(0)


if __name__ == '__main__':
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'ci/trace_events.csv'
    check_skipped_task(csv_path)
