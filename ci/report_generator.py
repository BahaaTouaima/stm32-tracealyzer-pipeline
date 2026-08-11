#!/usr/bin/env python3
"""
ci/report_generator.py

E7-01: Build the final HTML report - summary, task names/timing per issue,
and trace evidence for each problem.

Input:
  - severity_report.csv  (written by severity_report.py)
  - trace_events.csv     (written by parse_events.py)

Output:
  - report.html
"""

import csv
import os
import bisect
import html
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
        return "<p class='no-evidence'>No trace evidence available for this finding.</p>"

    header_cells = "".join(
        f"<th>{html.escape(h)}</th>"
        for h in ["timestamp_ms", "event_name", "task_name", "task_state", "param2_raw"]
    )
    body_rows = []
    for ev in evidence_rows:
        cells = "".join(
            f"<td>{html.escape(str(ev.get(col, '')))}</td>"
            for col in ["timestamp_ms", "event_name", "task_name", "task_state", "param2_raw"]
        )
        body_rows.append(f"<tr>{cells}</tr>")

    return (
        "<table class='evidence-table'>"
        f"<thead><tr>{header_cells}</tr></thead>"
        f"<tbody>{''.join(body_rows)}</tbody>"
        "</table>"
    )


def render_finding(finding, evidence_rows):
    sev = finding["severity"]
    ts_display = f"{finding['timestamp_ms']}ms" if finding["timestamp_ms"] is not None else "N/A"
    recommendation = RECOMMENDATIONS.get(finding["problem_type"], "Review this finding manually.")

    return f"""
    <div class="finding finding-{html.escape(sev)}">
      <div class="finding-header">
        <span class="badge badge-{html.escape(sev)}">{html.escape(sev.upper())}</span>
        <span class="problem-type">{html.escape(finding['problem_type'])}</span>
        <span class="timestamp">t = {html.escape(ts_display)}</span>
      </div>
      <p class="description">{html.escape(finding['description'])}</p>
      <p class="recommendation"><strong>Recommendation:</strong> {html.escape(recommendation)}</p>
      <details>
        <summary>Trace evidence (&plusmn;{EVIDENCE_WINDOW_MS}ms)</summary>
        {render_evidence_table(evidence_rows)}
      </details>
    </div>
    """


def render_summary(findings):
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1

    badges = "".join(
        f"<div class='summary-card summary-{sev}'><span class='count'>{counts[sev]}</span>"
        f"<span class='label'>{sev.capitalize()}</span></div>"
        for sev in ["critical", "high", "medium", "low"]
    )
    return f"<div class='summary-grid'>{badges}</div>"


def render_report(findings, trace_rows, trace_timestamps):
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    findings_html = []
    for finding in findings:
        if finding["problem_type"] in NO_TIMESTAMP_TYPES:
            evidence = []
        else:
            evidence = get_evidence(finding["timestamp_ms"], trace_rows, trace_timestamps)
        findings_html.append(render_finding(finding, evidence))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>STM32 FreeRTOS Stress Test Report</title>
<style>
  body {{ font-family: -apple-system, Arial, sans-serif; background:#f5f6f8; color:#1c1e21; margin:0; padding:2rem; }}
  h1 {{ margin-bottom:0.2rem; }}
  .meta {{ color:#666; margin-bottom:1.5rem; }}
  .summary-grid {{ display:flex; gap:1rem; margin-bottom:2rem; }}
  .summary-card {{ flex:1; padding:1rem; border-radius:8px; text-align:center; color:#fff; }}
  .summary-card .count {{ display:block; font-size:2rem; font-weight:bold; }}
  .summary-critical {{ background:#8b0000; }}
  .summary-high {{ background:#d9534f; }}
  .summary-medium {{ background:#f0ad4e; }}
  .summary-low {{ background:#5bc0de; }}
  .finding {{ background:#fff; border-left:6px solid #ccc; border-radius:6px; padding:1rem 1.2rem; margin-bottom:1rem; box-shadow:0 1px 2px rgba(0,0,0,0.08); }}
  .finding-critical {{ border-left-color:#8b0000; }}
  .finding-high {{ border-left-color:#d9534f; }}
  .finding-medium {{ border-left-color:#f0ad4e; }}
  .finding-low {{ border-left-color:#5bc0de; }}
  .finding-header {{ display:flex; align-items:center; gap:0.75rem; margin-bottom:0.5rem; }}
  .badge {{ font-size:0.75rem; font-weight:bold; padding:0.2rem 0.5rem; border-radius:4px; color:#fff; }}
  .badge-critical {{ background:#8b0000; }}
  .badge-high {{ background:#d9534f; }}
  .badge-medium {{ background:#f0ad4e; }}
  .badge-low {{ background:#5bc0de; }}
  .problem-type {{ font-weight:600; }}
  .timestamp {{ margin-left:auto; color:#666; font-size:0.9rem; }}
  .description {{ margin:0.3rem 0; }}
  .recommendation {{ font-size:0.9rem; color:#333; }}
  details {{ margin-top:0.5rem; }}
  summary {{ cursor:pointer; font-size:0.85rem; color:#0645ad; }}
  .evidence-table {{ width:100%; border-collapse:collapse; margin-top:0.5rem; font-size:0.8rem; }}
  .evidence-table th, .evidence-table td {{ border:1px solid #ddd; padding:0.3rem 0.5rem; text-align:left; }}
  .evidence-table th {{ background:#f0f0f0; }}
  .no-evidence {{ font-size:0.85rem; color:#888; font-style:italic; }}
</style>
</head>
<body>
  <h1>STM32 FreeRTOS Stress Test &amp; Weakness Report</h1>
  <p class="meta">Generated {html.escape(generated_at)} &middot; {len(findings)} finding(s)</p>
  {render_summary(findings)}
  <h2>Findings</h2>
  {''.join(findings_html)}
</body>
</html>
"""


def main():
    raw_findings = load_findings()
    findings = parse_findings(raw_findings)
    trace_rows, trace_timestamps = load_trace_events()

    report_html = render_report(findings, trace_rows, trace_timestamps)

    out_path = os.path.join(SCRIPT_DIR, "report.html")
    with open(out_path, "w") as f:
        f.write(report_html)

    print(f"Report generated with {len(findings)} finding(s).")
    print(f"Written to: {out_path}")


if __name__ == "__main__":
    main()
