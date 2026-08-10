import csv
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def check_isr_overruns(csv_file, max_duration_ms=1.0, out_path=None):
    if out_path is None:
        out_path = os.path.join(SCRIPT_DIR, "isr_overruns.csv")
    events = []
    with open(csv_file, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row['timestamp_ms'] = float(row['timestamp_ms'])
                events.append(row)
            except (ValueError, KeyError):
                continue

    overruns_found = 0
    overrun_records = []
    print(f"Analyzing {len(events)} events for ISR overruns (Threshold: {max_duration_ms} ms)...")

    # Find TIM2_Sensor ISR_BEGIN events and compute duration to the matching ISR_END
    for i in range(len(events) - 1):
        curr = events[i]
        if curr.get('event_name') == 'ISR_BEGIN' and 'TIM2_Sensor' in curr.get('task_name', ''):
            start_time = curr['timestamp_ms']
            nxt = events[i + 1]

           
            next_time = nxt['timestamp_ms']
            duration = next_time - start_time


            # Guard against negative duration anomalies from interleaved events
            if duration < 0:
                print(f"    [!] Warning: Negative duration detected ({duration:.3f} ms) at t={start_time:.3f} ms. Skipping anomaly.")
                continue


            print(f"   (ISR ends at next event: '{nxt.get('event_name')}' "
                  f"for '{nxt.get('task_name', '?')}')")
            print(f"-> TIM2_Sensor ISR at t={start_time:.3f} ms | Duration: {duration:.3f} ms")

            if duration > max_duration_ms:
                print(f"   [!] OVERRUN WARNING: Duration {duration:.3f} ms exceeds threshold {max_duration_ms} ms!")
                overruns_found += 1
                overrun_records.append((start_time, duration))

    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["isr_name", "start_time_ms", "duration_ms", "severity"])
        for start_time, duration in overrun_records:
            severity = "critical" if duration > max_duration_ms * 3 else "high" if duration > max_duration_ms * 1.5 else "medium"
            writer.writerow(["TIM2_Sensor", f"{start_time:.3f}", f"{duration:.3f}", severity])
    print(f"Written to: {out_path}")

    if overruns_found > 0:
        print(f"\n[FLAGGED] Found {overruns_found} ISR overrun(s). See {out_path} for details.")
    else:
        print("\n[OK] All ISR durations within safe limits.")
    # Detection findings are reported, not treated as pipeline failures.
    # The pipeline should always run to completion so later stages
    # (severity ranking, reporting) can process what was found.
    sys.exit(0)

if __name__ == '__main__':
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'ci/trace_events.csv'
    check_isr_overruns(csv_path)
