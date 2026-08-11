#!/usr/bin/env python3
"""
ci/report_generator.py

E7-01: Build the final Markdown report - summary, task names/timing per
issue, and trace evidence for each problem.

Input:
  - severity_report.csv  (written by severity_report.py)
  - trace_events.csv     (written by parse_events.py)

Output:
  - report.md
"""

import csv
import os
import bisect
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

SEVERITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}

EVIDENCE_WINDOW_MS = 20

NO_TIMESTAMP_TYPES = {"cpu_hog", "low_stack"}

RECOMMENDATIONS = {
    "cpu_hog": "Profile the task for busy-wait loops or missing blocking calls "
               "(e.g. vTaskDelay, queue/semaphore waits) that could free up CPU time.",
    "isr_overrun": "Shorten the ISR body - move non-critical work to a deferred task "
                   "(e.g. via a queue or task notification) instead of doing it in the ISR.",
    "priority_inversion": "Consider a priority inheritance mutex instead of a plain "
                           "semaphore, or shorten the critical section held by the low-priority task.",
    "missed_deadline": "Review the task's priority and the load of higher-priority tasks "
                        "running around this time; the deadline task may be getting starved.",
    "low_stack": "Increase the allocated stack size for this task, or reduce local "
                 "variable / call-depth usage inside it.",
    "skipped_task": "Check for higher-priority tasks monopolizing the CPU during this "
                     "window; consider raising this task's priority or adding time slicing.",
}


def read_csv_rows(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def load_findings():
    path = os.path.join(SCRIPT_DIR, "severity_report.csv")
    rows = read_csv_rows(path)
    if not rows:
        print(f"WARNING: no findings found at {path}")
    return rows


def load_trace_events():
    path = os.path.join(SCRIPT_DIR, "trace_events.csv")
    rows = read_csv_rows(path)
    timestamps = []
    for row in rows:
        try:
            timestamps.append(float(row["timestamp_ms"]))
        except (ValueError, KeyError):
            timestamps.append(float("inf"))
    return rows, timestamps


def get_evidence(target_ts, rows, timestamps, window_ms=EVIDENCE_WINDOW_MS):
    if target_ts is None or not rows:
        return []
    lo_bound = target_ts - window_ms
    hi_bound = target_ts + window_ms
    lo = bisect.bisect_left(timestamps, lo_bound)
    hi = bisect.bisect_right(timestamps, hi_bound)
    return rows[lo:hi]


def parse_findings(raw_findings):
    parsed = []
    for row in raw_findings:
        ts_raw = row.get("timestamp_ms", "")
        try:
            ts = float(ts_raw) if ts_raw not in (None, "") else None
        except ValueError:
            ts = None
        parsed.append({
            "severity": row.get("severity", "low"),
            "problem_type": row.get("problem_type", ""),
            "description": row.get("description", ""),
            "timestamp_ms": ts,
        })
    parsed.sort(key=lambda f: (SEVERITY_RANK.get(f["severity"], 99),
                                f["timestamp_ms"] if f["timestamp_ms"] is not None else float("inf")))
    return parsed


def render_evidence_table(evidence_rows):
    if not evidence_rows:
        return "_No trace evidence available for this finding._"

    cols = ["timestamp_ms", "event_name", "task_name", "task_state", "param2_raw"]
    header = "| " + " | ".join(cols) + " |"
    separator = "| " + " | ".join("---" for _ in cols) + " |"
    body_lines = []
    for ev in evidence_rows:
        cells = [str(ev.get(col, "")).replace("|", "\\|") for col in cols]
        body_lines.append("| " + " | ".join(cells) + " |")

    return "\n".join([header, separator] + body_lines)


def render_finding(index, finding, evidence_rows):
    sev = finding["severity"]
    ts_display = f"{finding['timestamp_ms']}ms" if finding["timestamp_ms"] is not None else "N/A"
    recommendation = RECOMMENDATIONS.get(finding["problem_type"], "Review this finding manually.")

    return f"""### {index}. [{sev.upper()}] {finding['problem_type']} — t = {ts_display}

**Description:** {finding['description']}

**Recommendation:** {recommendation}

<details>
<summary>Trace evidence (&plusmn;{EVIDENCE_WINDOW_MS}ms)</summary>

{render_evidence_table(evidence_rows)}

</details>

---
"""


def render_summary(findings):
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1

    lines = ["| Severity | Count |", "|---|---|"]
    for sev in ["critical", "high", "medium", "low"]:
        lines.append(f"| {sev.capitalize()} | {counts[sev]} |")
    return "\n".join(lines)


def render_report(findings, trace_rows, trace_timestamps):
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    findings_lines = []
    for i, finding in enumerate(findings, start=1):
        if finding["problem_type"] in NO_TIMESTAMP_TYPES:
            evidence = []
        else:
            evidence = get_evidence(finding["timestamp_ms"], trace_rows, trace_timestamps)
        findings_lines.append(render_finding(i, finding, evidence))

    findings_section = "\n".join(findings_lines) if findings_lines else "_No findings._"

    return f"""# STM32 FreeRTOS Stress Test & Weakness Report

_Generated {generated_at} &middot; {len(findings)} finding(s)_

## Summary

{render_summary(findings)}

## Findings

{findings_section}
"""


def main():
    raw_findings = load_findings()
    findings = parse_findings(raw_findings)
    trace_rows, trace_timestamps = load_trace_events()

    report_md = render_report(findings, trace_rows, trace_timestamps)

    out_path = os.path.join(SCRIPT_DIR, "report.md")
    with open(out_path, "w") as f:
        f.write(report_md)

    print(f"Report generated with {len(findings)} finding(s).")
    print(f"Written to: {out_path}")


if __name__ == "__main__":
    main()
