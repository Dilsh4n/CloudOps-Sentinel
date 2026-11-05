#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_ROOT"

echo "Starting cloudops sentinel verification"

# check development environment
./scripts/check_environment.sh

# run python smoke test
python scripts/smoke_test.py --url "${1:-http://127.0.0.1:8000}"

echo "[PASS] all verification checks passed!"