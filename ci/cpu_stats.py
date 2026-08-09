#!/usr/bin/env python3
"""
E5-01: Compute per-task CPU utilization from trace_events.csv.
"""

import csv
import sys
from collections import defaultdict

COL_TIMESTAMP = "timestamp_ms"
COL_TASK = "task_name"
COL_STATE = "task_state"
RUNNING_STATE = "RUNNING"


def compute_cpu_utilization(csv_path):
    rows = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    if not rows:
        print("No events found in trace file.")
        return {}, 0

    rows.sort(key=lambda r: float(r[COL_TIMESTAMP]))
    trace_start = float(rows[0][COL_TIMESTAMP])
    trace_end = float(rows[-1][COL_TIMESTAMP])
    total_duration = trace_end - trace_start

    if total_duration <= 0:
        print("Trace duration is zero or negative -- check timestamps.")
        return {}, 0

    activations = [
        (float(r[COL_TIMESTAMP]), r[COL_TASK].strip())
        for r in rows
        if r.get(COL_STATE, "").strip().upper() == RUNNING_STATE and r.get(COL_TASK, "").strip()
    ]

    running_time = defaultdict(float)
    for i in range(len(activations) - 1):
        ts, task = activations[i]
        next_ts, _ = activations[i + 1]
        running_time[task] += next_ts - ts

    if activations:
        last_ts, last_task = activations[-1]
        running_time[last_task] += trace_end - last_ts

    cpu_percent = {t: (v / total_duration) * 100.0 for t, v in running_time.items()}
    return cpu_percent, total_duration


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 compute_cpu_stats.py <trace_events.csv> [output_csv]")
        sys.exit(1)

    csv_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "cpu_utilization.csv"

    cpu_percent, total_duration = compute_cpu_utilization(csv_path)
    if not cpu_percent:
        sys.exit(1)

    print(f"Trace duration: {total_duration}")
    print("Per-task CPU utilization:")
    for task, pct in sorted(cpu_percent.items(), key=lambda x: -x[1]):
        print(f"  {task:20s} {pct:6.2f}%")

    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["task_name", "cpu_percent"])
        for task, pct in sorted(cpu_percent.items(), key=lambda x: -x[1]):
            writer.writerow([task, f"{pct:.2f}"])

    print(f"Written to: {out_path}")


if __name__ == "__main__":
    main()
