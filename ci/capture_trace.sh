#!/bin/bash
# ci/capture_trace.sh
# Runs the firmware in QEMU, lets it execute for a while so trace events
# accumulate in memory, then uses GDB to dump that memory into a real
# file on the host machine.

OUTPUT_DIR=~/stm32-tracealyzer-pipeline/firmware/build/gcc/output
BINARY=RTOSDemo.out
TRACE_FILE=~/stm32-tracealyzer-pipeline/ci/trace.bin
QEMU_LOG=~/stm32-tracealyzer-pipeline/ci/qemu_output.log

START_ADDR=0x20019c60
END_ADDR=0x2001d258

cd "$OUTPUT_DIR" || exit 1

echo "[1] Starting QEMU in the background..."
qemu-system-arm -M mps2-an385 -kernel $BINARY -nographic -monitor none -s > "$QEMU_LOG" 2>&1 &
QEMU_PID=$!

echo "[2] Letting firmware run for 10 seconds..."
sleep 10

echo "[3] Connecting GDB and dumping memory..."
gdb-multiarch -batch \
  -ex "target remote :1234" \
  -ex "dump binary memory $TRACE_FILE $START_ADDR $END_ADDR" \
  -ex "detach" \
  $BINARY

echo "[4] Stopping QEMU..."
kill $QEMU_PID 2>/dev/null

echo "[5] Done. Trace should be at: $TRACE_FILE"
