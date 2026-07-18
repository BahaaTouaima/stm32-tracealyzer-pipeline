#!/bin/bash
# ci/pipeline.sh
# Pipeline entry point: fetches the latest code and logs each run.
# Later stories (E3-03 webhook, E3-04 cppcheck) will extend this script.

PROJECT_DIR="$HOME/stm32-tracealyzer-pipeline"
LOG_FILE="$PROJECT_DIR/ci/pipeline.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Pipeline run started" >> "$LOG_FILE"

cd "$PROJECT_DIR" || { echo "[$TIMESTAMP] ERROR: project directory not found" >> "$LOG_FILE"; exit 1; }

git pull origin main >> "$LOG_FILE" 2>&1

echo "[$TIMESTAMP] Pipeline run finished" >> "$LOG_FILE"
