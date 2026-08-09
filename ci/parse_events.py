import struct
import sys
import csv
import re
import os

# offset ou commencent les vrais events dans trace.bin (trouve avec gdb)
# avant ça: header PSF + timestamp info + table des noms
HEADER_SIZE = 2808



# freq du timer + diviseur, pour convertir le timestamp en ms
CPU_CLOCK_HZ = 25000000
HWTC_DIVISOR = 4

# position + taille de la table des noms de taches dans trace.bin
ENTRY_TABLE_FILE_OFFSET = 72
ENTRY_SIZE = 48          # taille d'une entree
ENTRY_COUNT = 56         # nombre d'entrees dans la table
SYMBOL_OFFSET_IN_ENTRY = 20   # ou commence le nom dans une entree
SYMBOL_SIZE = 28              # taille max du nom


def load_entry_table_names(data):
    # lit la entry table et retourne un dict {handle: nom}

    names = {}
    for i in range(ENTRY_COUNT):
        entry_start = ENTRY_TABLE_FILE_OFFSET + (i * ENTRY_SIZE)

        # 4 premiers octets = adresse handle de la tache
        handle = struct.unpack_from("<I", data, entry_start)[0]

        symbol_start = entry_start + SYMBOL_OFFSET_IN_ENTRY
        raw_symbol = data[symbol_start: symbol_start + SYMBOL_SIZE]

        # coupe au premier octet nul (fin de string en C), puis decode en texte
        name = raw_symbol.split(b"\x00")[0].decode(errors="replace")

        # ignore les entrees vides
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


# chemin vers trcKernelPort.h, calcule a partir du script lui meme

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
KERNEL_PORT_HEADER = os.path.join(
    PROJECT_ROOT, "firmware", "TraceRecorder", "kernelports",
    "FreeRTOS", "include", "trcKernelPort.h"
)


def load_event_names(header_path):
    # lit trcKernelPort.h et construit un dict {code: nom_event}
    # a partir des lignes #define PSF_EVENT_XXX 0xYY

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
    # les 4 bits du haut de event_id = nombre de parametres
    return (event_id >> 12) & 0xF


def get_base_event_id(event_id):
    # les 12 bits du bas de event_id = le vrai type d'event
    return event_id & 0x0FFF








SYSTICK_PERIOD = 25000  # verified: configSYSTICK_CLOCK_HZ(25000000)/configTICK_RATE_HZ(1000)

def decode_packed_timestamp(raw_ts, prev_tick_low8, wrap_count):
    hwtc_value = raw_ts & 0x00FFFFFF
    tick_low8 = (raw_ts >> 24) & 0xFF
    if prev_tick_low8 is not None and tick_low8 < prev_tick_low8:
        wrap_count += 1
    full_tick_count = wrap_count * 256 + tick_low8
    fraction = (SYSTICK_PERIOD - hwtc_value) / SYSTICK_PERIOD
    ms = full_tick_count + fraction
    return ms, tick_low8, wrap_count








def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "trace.bin"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "trace_events.csv"

    # charge la liste des types d'events une seule fois
    event_names = load_event_names(KERNEL_PORT_HEADER)
    print(f"Loaded {len(event_names)} event type names from {KERNEL_PORT_HEADER}")

    # lit tout le fichier binair
    with open(path, "rb") as f:
        data = f.read()

    # charge la table des noms de taches une seule fois
    handle_to_name = load_entry_table_names(data)
    print(f"Loaded {len(handle_to_name)} names from the entry table: {list(handle_to_name.values())}")

    rows = []
    offset = HEADER_SIZE  # position de lecture, avance a chaque event

    prev_tick_low8 = None
    wrap_count = 0

    # lit un event a la fois jusqu'a la fin du fichier
    while offset + 8 <= len(data):
        # lit les 8 octets de base de tout event: id + count + timestamp
        event_id, event_count, ts = struct.unpack_from("<HHI", data, offset)

        param_count = get_param_count(event_id)
        base_id = get_base_event_id(event_id)

        # taille reelle de cet event: 8 octets + 4 par parametre
        event_size = 8 + (param_count * 4)

        # si l'event depasse la fin du fichier, on arrete (evite crash)
        if offset + event_size > len(data):
            break

        # nom lisible de l'even
        event_name = event_names.get(base_id, hex(base_id))
        ms_raw, prev_tick_low8, wrap_count = decode_packed_timestamp(ts, prev_tick_low8, wrap_count)
        ms = round(ms_raw, 3)

        # si l'event a un parametre, souvent c'est un handle de tache
        # on essaie de le resoudre en vrai nom. certains events (delay)
        # ont un parametre qui est pas un handle, dans ce cas task_name
        # reste juste vide, pas d'erreur
        if param_count >= 1:
            handle = struct.unpack_from("<I", data, offset + 8)[0]
            task_name = handle_to_name.get(handle, "")
        else:
            task_name = ""

        # etat simplifie si connu pour ce type d'event
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

        offset += event_size  # passe a l'event suivant

    # ecrit tous les events dans le csv final
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Parsed {len(rows)} events.")
    print(f"Resolved {len(handle_to_name)} task/object names: {list(handle_to_name.values())}")
    print(f"Written to: {out_path}")


if __name__ == "__main__":
    main()
