#!/usr/bin/env python3
"""
E6-07: Flag tasks exceeding a CPU usage threshold.
Reads cpu_utilization.csv (from cpu_stats.py) and flags any task
whose cpu_percent exceeds CPU_THRESHOLD_PERCENT.
"""

import csv
import sys

CPU_THRESHOLD_PERCENT = 50.0  # adjust based on your system's expected load


"""def flag_cpu_hogs(csv_path, threshold):
    flagged = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            task = row["task_name"]
            pct = float(row["cpu_percent"])
            if pct > threshold:
                flagged.append((task, pct))
    return flagged
"""

EXCLUDED_TASKS = {"IDLE"}  # high idle % is healthy, not a weakness

def flag_cpu_hogs(csv_path, threshold):
    flagged = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            task = row["task_name"]
            if task in EXCLUDED_TASKS:
                continue
            pct = float(row["cpu_percent"])
            if pct > threshold:
                flagged.append((task, pct))
    return flagged



def main():
    if len(sys.argv) < 2:
        print("Usage: python3 cpu_flag.py <cpu_utilization.csv> [output_csv]")
        sys.exit(1)

    csv_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "cpu_flags.csv"

    flagged = flag_cpu_hogs(csv_path, CPU_THRESHOLD_PERCENT)

    if flagged:
        print(f"Flagged {len(flagged)} task(s) exceeding {CPU_THRESHOLD_PERCENT}% CPU:")
        for task, pct in flagged:
            print(f"  {task:20s} {pct:6.2f}%  [FLAGGED]")
    else:
        print(f"No tasks exceeded {CPU_THRESHOLD_PERCENT}% CPU.")

    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["task_name", "cpu_percent", "severity"])
        for task, pct in flagged:
            severity = "critical" if pct > 80 else "high" if pct > 65 else "medium"
            writer.writerow([task, f"{pct:.2f}", severity])

    print(f"Written to: {out_path}")


if __name__ == "__main__":
    main()
