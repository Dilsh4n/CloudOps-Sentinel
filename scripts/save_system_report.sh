#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_ROOT"

REPORT_DIR="$PROJECT_ROOT/reports"
REPORT_FILE="$REPORT_DIR/system_info.json"

mkdir -p "$REPORT_DIR"

TEMP_FILE="$(mktemp "$REPORT_DIR/systeminfo.json.XXXXXX")"

trap "rm -f $TEMP_FILE" EXIT

echo "[INFO] collecting system information"
python scripts/collect_system_info.py > "$TEMP_FILE"
echo "[INFO] validating JSON report"

python -m json.tool "$TEMP_FILE" > /dev/null

mv "$TEMP_FILE" "$REPORT_FILE"

echo "[PASS] system report saved to $REPORT_FILE"