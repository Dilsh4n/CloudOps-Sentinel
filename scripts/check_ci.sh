#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"

cd "$PROJECT_ROOT"

echo "=================================="
echo "CloudOps Sentinel CI Verification"
echo "=================================="

echo "[1/4] Checking Bash syntax..."
bash -n scripts/*.sh

echo "[2/4] Checking Python syntax..."
python -m compileall -q app scripts

echo "[3/4] Running Python lint checks..."
python -m ruff check app scripts tests

echo "[4/4] Running automated tests..."
python -m pytest -q

echo "=================================="
echo "[PASS] All CI checks passed!"