import csv
import sys

def check_blocking_chains(csv_file, max_block_ms=100.0, out_path="ci/blocking_chains.csv"):
    events = []
    with open(csv_file, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row['timestamp_ms'] = float(row['timestamp_ms'])
                events.append(row)
            except (ValueError, KeyError):
                continue

    print(f"Analyzing {len(events)} events for priority-inheritance blocking chains "
          f"(threshold: {max_block_ms} ms)...")

    open_inherits = {}   # task_name -> start_time_ms
    chains_found = []

    for row in events:
        ev = row.get('event_name')
        name = row.get('task_name', '')
        t = row['timestamp_ms']

        if ev == 'TASK_PRIO_INHERIT' and name:
            open_inherits[name] = t
        elif ev == 'TASK_PRIO_DISINHERIT' and name and name in open_inherits:
            start = open_inherits.pop(name)
            duration = t - start
            chains_found.append((name, start, duration))
            print(f"-> Blocking chain: '{name}' held resource, blocking a higher-priority "
                  f"task from t={start:.3f}ms to t={t:.3f}ms (duration {duration:.3f}ms)")

    # Any inherit that never got a matching disinherit in this trace window
    for name, start in open_inherits.items():
        print(f"   [!] WARNING: '{name}' inherited priority at t={start:.3f}ms but no "
              f"matching TASK_PRIO_DISINHERIT found in this trace window -- "
              f"possibly still blocked when capture ended.")

    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["blocking_task", "start_time_ms", "duration_ms", "severity"])
        for name, start, duration in chains_found:
            severity = ("critical" if duration > max_block_ms * 3
                        else "high" if duration > max_block_ms
                        else "low")
            writer.writerow([name, f"{start:.3f}", f"{duration:.3f}", severity])
    print(f"Written to: {out_path}")

    long_blocks = [c for c in chains_found if c[2] > max_block_ms]
    if long_blocks:
        print(f"\n[FAIL] Found {len(long_blocks)} blocking chain(s) exceeding {max_block_ms}ms.")
        sys.exit(1)
    elif chains_found:
        print(f"\n[PASS] Found {len(chains_found)} blocking chain(s), all within {max_block_ms}ms threshold.")
        sys.exit(0)
    else:
        print("\n[PASS] No blocking chains detected in this trace.")
        sys.exit(0)

if __name__ == '__main__':
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'ci/trace_events.csv'
    check_blocking_chains(csv_path)
