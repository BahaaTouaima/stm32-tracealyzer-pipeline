import csv
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Allocated stack size per task, in words (matches xTaskCreate calls in main_blinky.c).
# Tasks not listed here default to DEFAULT_STACK_WORDS.
DEFAULT_STACK_WORDS = 128   # configMINIMAL_STACK_SIZE
TASK_STACK_SIZES_WORDS = {
    "TzCtrl": 256,          # TRC_CFG_CTRL_TASK_STACK_SIZE
}

REMAINING_THRESHOLD_PERCENT = 50.0   # flag if remaining stack drops below this


def check_stack_watermarks(csv_file, threshold_percent=REMAINING_THRESHOLD_PERCENT, out_path=None):
    if out_path is None:
        out_path = os.path.join(SCRIPT_DIR, "stack_flags.csv")

    events = []
    with open(csv_file, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row['timestamp_ms'] = float(row['timestamp_ms'])
                events.append(row)
            except (ValueError, KeyError):
                continue

    print(f"Analyzing {len(events)} events for low stack watermarks "
          f"(threshold: remaining stack below {threshold_percent}%)...")

    # Keep only the lowest watermark seen per task across the whole trace.
    lowest_watermark_words = {}

    for row in events:
        if row.get('event_name') != 'UNUSED_STACK':
            continue
        task = row.get('task_name', '')
        raw = row.get('param2_raw', '')
        if not task or raw == '':
            continue
        try:
            words = int(raw)
        except ValueError:
            continue
        if task not in lowest_watermark_words or words < lowest_watermark_words[task]:
            lowest_watermark_words[task] = words

    flagged = []
    for task, words in sorted(lowest_watermark_words.items()):
        allocated_words = TASK_STACK_SIZES_WORDS.get(task, DEFAULT_STACK_WORDS)
        allocated_bytes = allocated_words * 4
        remaining_bytes = words * 4
        percent_remaining = (words / allocated_words) * 100.0

        print(f"-> {task:15s} lowest watermark: {words:4d} words ({remaining_bytes} bytes) "
              f"of {allocated_words} words ({allocated_bytes} bytes) allocated "
              f"= {percent_remaining:.1f}% remaining")

        if percent_remaining < threshold_percent:
            print(f"   [!] LOW STACK WARNING: {task} has only {percent_remaining:.1f}% "
                  f"stack remaining (below {threshold_percent}% threshold)!")
            flagged.append((task, words, allocated_words, remaining_bytes, allocated_bytes, percent_remaining))

    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["task_name", "watermark_words", "allocated_words",
                          "remaining_bytes", "allocated_bytes", "percent_remaining", "severity"])
        for task, words, alloc_words, rem_bytes, alloc_bytes, pct in flagged:
            severity = ("critical" if pct < threshold_percent * 0.3
                        else "high" if pct < threshold_percent * 0.6
                        else "medium")
            writer.writerow([task, words, alloc_words, rem_bytes, alloc_bytes,
                              f"{pct:.1f}", severity])

    print(f"Written to: {out_path}")

    if flagged:
        print(f"\n[FLAGGED] Found {len(flagged)} task(s) with low stack watermarks. "
              f"See {out_path} for details.")
    else:
        print("\n[OK] All tasks have healthy stack margins.")
    # Detection findings are reported, not treated as pipeline failures.
    sys.exit(0)


if __name__ == '__main__':
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'ci/trace_events.csv'
    check_stack_watermarks(csv_path)
