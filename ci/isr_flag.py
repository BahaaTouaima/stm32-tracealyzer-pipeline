import csv
import sys

def check_isr_overruns(csv_file, max_duration_ms=1.0):
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
    print(f"Analyzing {len(events)} events for ISR overruns (Threshold: {max_duration_ms} ms)...")

    # Find TIM2_Sensor events and compute duration to the subsequent event
    for i in range(len(events) - 1):
        curr = events[i]
        if curr.get('event_name') == 'ISR_BEGIN' and 'TIM2_Sensor' in curr.get('task_name', ''):
            start_time = curr['timestamp_ms']
            next_time = events[i + 1]['timestamp_ms']
            duration = next_time - start_time

            print(f"-> TIM2_Sensor ISR at t={start_time:.3f} ms | Duration: {duration:.3f} ms")

            if duration > max_duration_ms:
                print(f"   [!] OVERRUN WARNING: Duration {duration:.3f} ms exceeds threshold {max_duration_ms} ms!")
                overruns_found += 1

    if overruns_found > 0:
        print(f"\n[FAIL] Found {overruns_found} ISR overrun(s).")
        sys.exit(1)
    else:
        print("\n[PASS] All ISR durations within safe limits.")
        sys.exit(0)

if __name__ == '__main__':
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'ci/trace_events.csv'
    check_isr_overruns(csv_path)
