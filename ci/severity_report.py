import csv
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

SEVERITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def read_csv_rows(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def build_findings():
    findings = []

    # cpu_flags.csv: task_name, cpu_percent, severity
    for row in read_csv_rows(os.path.join(SCRIPT_DIR, "cpu_flags.csv")):
        findings.append({
            "problem_type": "cpu_hog",
            "description": f"Task '{row['task_name']}' used {row['cpu_percent']}% CPU",
            "severity": row.get("severity", "low"),
            "timestamp_ms": None,
        })

    # isr_overruns.csv: isr_name, start_time_ms, duration_ms, severity
    for row in read_csv_rows(os.path.join(SCRIPT_DIR, "isr_overruns.csv")):
        findings.append({
            "problem_type": "isr_overrun",
            "description": f"ISR '{row['isr_name']}' ran for {row['duration_ms']}ms "
                            f"(started t={row['start_time_ms']}ms)",
            "severity": row.get("severity", "low"),
            "timestamp_ms": row.get("start_time_ms"),
        })

    # blocking_chains.csv: blocking_task, start_time_ms, duration_ms, severity
    for row in read_csv_rows(os.path.join(SCRIPT_DIR, "blocking_chains.csv")):
        findings.append({
            "problem_type": "priority_inversion",
            "description": f"Task '{row['blocking_task']}' blocked a higher-priority task "
                            f"for {row['duration_ms']}ms (t={row['start_time_ms']}ms)",
            "severity": row.get("severity", "low"),
            "timestamp_ms": row.get("start_time_ms"),
        })

    # deadline_misses.csv: expected_start_ms, actual_start_ms, delay_ms, severity
    for row in read_csv_rows(os.path.join(SCRIPT_DIR, "deadline_misses.csv")):
        findings.append({
            "problem_type": "missed_deadline",
            "description": f"Deadline task started {row['delay_ms']}ms late "
                            f"(expected t={row['expected_start_ms']}ms, "
                            f"actual t={row['actual_start_ms']}ms)",
            "severity": row.get("severity", "low"),
            "timestamp_ms": row.get("actual_start_ms"),
        })

    # stack_flags.csv: task_name, watermark_words, allocated_words, remaining_bytes, allocated_bytes, percent_remaining, severity
    for row in read_csv_rows(os.path.join(SCRIPT_DIR, "stack_flags.csv")):
        findings.append({
            "problem_type": "low_stack",
            "description": f"Task '{row['task_name']}' has only {row['percent_remaining']}% "
                            f"stack remaining ({row['remaining_bytes']} of {row['allocated_bytes']} bytes)",
            "severity": row.get("severity", "low"),
            "timestamp_ms": None,
        })

    # skip_flags.csv: ready_time_ms, activate_time_ms, delay_ms, severity
    for row in read_csv_rows(os.path.join(SCRIPT_DIR, "skip_flags.csv")):
        findings.append({
            "problem_type": "skipped_task",
            "description": f"Task waited {row['delay_ms']}ms to run after becoming ready "
                            f"(t={row['ready_time_ms']}ms)",
            "severity": row.get("severity", "low"),
            "timestamp_ms": row.get("ready_time_ms"),
        })

    return findings


def sort_key(finding):
    rank = SEVERITY_RANK.get(finding["severity"], 99)
    ts = finding["timestamp_ms"]
    try:
        ts_val = float(ts) if ts not in (None, "") else float("inf")
    except ValueError:
        ts_val = float("inf")
    return (rank, ts_val)


def main():
    out_path = os.path.join(SCRIPT_DIR, "severity_report.csv")

    findings = build_findings()
    findings.sort(key=sort_key)

    print(f"Consolidated {len(findings)} finding(s) across all detectors, ranked by severity:\n")

    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for f in findings:
        sev = f["severity"]
        counts[sev] = counts.get(sev, 0) + 1
        print(f"[{sev.upper():8s}] {f['problem_type']:20s} {f['description']}")

    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["severity", "problem_type", "description", "timestamp_ms"])
        for finding in findings:
            writer.writerow([finding["severity"], finding["problem_type"],
                              finding["description"], finding["timestamp_ms"] or ""])

    print(f"\nSummary: {counts['critical']} critical, {counts['high']} high, "
          f"{counts['medium']} medium, {counts['low']} low.")
    print(f"Written to: {out_path}")

    # Reporting step, not a pipeline gate.
    sys.exit(0)


if __name__ == '__main__':
    main()
