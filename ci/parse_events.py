import struct
import sys
import csv
import re
import os

HEADER_SIZE = 2808  # confirmed via GDB: puiBuffer address minus header address
OBJ_NAME_EVENT = 0x03  # PSF_EVENT_OBJ_NAME -- kept for reference, but NOT used to resolve
                        # names in this streamport config: TRC_SEND_NAME_ONLY_ON_DELETE=1
                        # means names are never sent as events at creation time.
                        # Instead, names live in a separate, persistent Entry Table --
                        # see load_entry_table_names() below.
CPU_CLOCK_HZ = 25000000
HWTC_DIVISOR = 4

# Entry table layout (confirmed via GDB against the running firmware):
ENTRY_TABLE_FILE_OFFSET = 72     # where the entry table starts in trace.bin
ENTRY_SIZE = 48                  # bytes per entry
ENTRY_COUNT = 56                 # number of slots (uxSlots)
SYMBOL_OFFSET_IN_ENTRY = 20      # where szSymbol starts, within one entry
SYMBOL_SIZE = 28                 # length of szSymbol

def load_entry_table_names(data):
    """
    Reads the Entry Table directly from the trace file and returns a
    dict of {address_handle: name}. This is needed because this specific
    streamport (RingBuffer) never sends OBJ_NAME events at task creation --
    names are stored once, persistently, in this table instead.
    """
    names = {}
    for i in range(ENTRY_COUNT):
        entry_start = ENTRY_TABLE_FILE_OFFSET + (i * ENTRY_SIZE)
        # first 4 bytes of each entry = pvAddress (the handle)
        handle = struct.unpack_from("<I", data, entry_start)[0]
        symbol_start = entry_start + SYMBOL_OFFSET_IN_ENTRY
        raw_symbol = data[symbol_start: symbol_start + SYMBOL_SIZE]
        name = raw_symbol.split(b"\x00")[0].decode(errors="replace")
        if handle != 0 and name:
            names[handle] = name
    return names

TASK_STATE_EVENTS = {
    0x30: "READY",       # PSF_EVENT_TASK_READY
    0x37: "RUNNING",     # PSF_EVENT_TASK_ACTIVATE
    0x7a: "DELAYED",     # PSF_EVENT_TASK_DELAY
    0x79: "DELAYED",     # PSF_EVENT_TASK_DELAY_UNTIL
    0x7b: "SUSPENDED",   # PSF_EVENT_TASK_SUSPEND
    0x7c: "RESUMED",     # PSF_EVENT_TASK_RESUME
}







SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
KERNEL_PORT_HEADER = os.path.join(
    PROJECT_ROOT, "firmware", "TraceRecorder", "kernelports", "FreeRTOS", "include", "trcKernelPort.h"
)


def load_event_names(header_path):
    names = {}
    pattern = re.compile(r"#define\s+PSF_EVENT_(\w+)\s+(0x[0-9A-Fa-f]+)")
    with open(header_path, "r") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                name, value = match.groups()
                names[int(value, 16)] = name
    return names

def get_param_count(event_id):
    return (event_id >> 12) & 0xF

def get_base_event_id(event_id):
    return event_id & 0x0FFF

def ts_to_ms(raw_ts):
    return (raw_ts * HWTC_DIVISOR) / CPU_CLOCK_HZ * 1000

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "trace.bin"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "trace_events.csv"

    event_names = load_event_names(KERNEL_PORT_HEADER)
    print(f"Loaded {len(event_names)} event type names from {KERNEL_PORT_HEADER}")

    with open(path, "rb") as f:
        data = f.read()

    offset = HEADER_SIZE
    handle_to_name = load_entry_table_names(data)
    print(f"Loaded {len(handle_to_name)} names from the entry table: {list(handle_to_name.values())}")
    rows = []

    while offset + 8 <= len(data):
        event_id, event_count, ts = struct.unpack_from("<HHI", data, offset)
        param_count = get_param_count(event_id)
        base_id = get_base_event_id(event_id)
        event_size = 8 + (param_count * 4)

        if offset + event_size > len(data):
            break

        event_name = event_names.get(base_id, hex(base_id))
        ms = round(ts_to_ms(ts), 3)

        if param_count >= 1:
            # first param is usually a task/object handle -- try to resolve it
            handle = struct.unpack_from("<I", data, offset + 8)[0]
            task_name = handle_to_name.get(handle, "")
        else:
            task_name = ""


        task_state = TASK_STATE_EVENTS.get(base_id, "")

        rows.append({
            "offset": offset,
            "event_id_hex": hex(base_id),
            "event_name": event_name,
            "event_count": event_count,
            "timestamp_ms": ms,
            "param_count": param_count,
            "task_name": task_name,
	    "task_state": task_state,
        })

        offset += event_size

    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Parsed {len(rows)} events.")
    print(f"Resolved {len(handle_to_name)} task/object names: {list(handle_to_name.values())}")
    print(f"Written to: {out_path}")

if __name__ == "__main__":
    main()
