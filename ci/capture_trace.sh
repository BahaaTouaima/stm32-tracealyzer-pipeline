#!/bin/bash
# ci/capture_trace.sh
# Runs the firmware in QEMU, lets it execute for a while so trace events
# accumulate in memory, then uses GDB to dump that memory into a real
# file on the host machine.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$PROJECT_ROOT/firmware/build/gcc/output"
BINARY=RTOSDemo.out
TRACE_FILE="$PROJECT_ROOT/ci/trace.bin"
QEMU_LOG="$PROJECT_ROOT/ci/qemu_output.log"



cd "$OUTPUT_DIR" || exit 1

echo "[1] Starting QEMU in the background..."
qemu-system-arm -M mps2-an385 -kernel $BINARY -nographic -monitor none -s  > "$QEMU_LOG" 2>&1 &
QEMU_PID=$!

echo "[2] waiting for gdb to connect..."
sleep 5

echo "[3] running until task created, then dumping memory..."
gdb-multiarch -batch \
  -ex "target remote :1234" \
-ex "dump binary memory $TRACE_FILE &pxStreamPortData->xRingBuffer.xHeaderBuffer (&pxStreamPortData->xRingBuffer.xEventBuffer + 1)" \
  -ex "detach" \
  $BINARY

echo "[4] Stopping QEMU..."
kill $QEMU_PID 2>/dev/null

echo "[5] Done. Trace should be at: $TRACE_FILE"
