#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_ROOT"

SERVICE="${1:-systemd-journald.service}"

echo "================================="
echo "CloudOps Sentinel Server Check"
echo "================================="

echo "[INFO] Service: $SERVICE"

if python3 scripts/diagnose_service.py \
    --service "$SERVICE" \
    --lines 5 \
    --top 5; then

    echo "[PASS] Diagnostic check completed successfully"

else
    echo "[FAIL] Service check failed" >&2
    exit 1
fi