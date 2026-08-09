#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$PROJECT_ROOT/firmware/build/gcc/output"
BINARY=RTOSDemo.out
TRACE_FILE="$PROJECT_ROOT/ci/trace.bin"
QEMU_LOG="$PROJECT_ROOT/ci/qemu_output.log"

cd "$OUTPUT_DIR" || exit 1

echo "[1] Starting QEMU (halted, waiting for gdb)..."
qemu-system-arm -M netduinoplus2 -kernel $BINARY -nographic -monitor none -s -S < /dev/null > "$QEMU_LOG" 2>&1 &
QEMU_PID=$!
sleep 1

echo "[2] Running target for ~5000 ticks, then dumping memory..."
gdb-multiarch -batch \
  -ex "target remote :1234" \
  -ex "break xPortSysTickHandler" \
  -ex "ignore 1 5000" \
  -ex "continue" \
  -ex "dump binary memory $TRACE_FILE &pxStreamPortData->xRingBuffer.xHeaderBuffer (&pxStreamPortData->xRingBuffer.xEventBuffer + 1)" \
  -ex "detach" \
  $BINARY

echo "[3] Stopping QEMU..."
kill $QEMU_PID 2>/dev/null

echo "[QEMU LOG]"
cat "$QEMU_LOG"
echo "[4] Done. Trace should be at: $TRACE_FILE"
