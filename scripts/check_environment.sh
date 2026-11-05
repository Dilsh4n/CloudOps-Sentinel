#!/usr/bin/env bash

set -euo pipefail
# -e errexit => exit if any unhandled command failure occur
# -u treat reference to unset variables as errors
# -o pipefail - make pipeline fail if any commands in it fails

echo "Checking CloudOps Sentinel environment..."

for tool in python3 git curl; do
    if command -v "$tool" > /dev/null 2>&1; then
        echo "[OK] $tool is installed"
    else
        echo "[ERROR] $tool is missing"
        exit 1
    fi
done

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
# -Z -> check whether a string is empty
    echo "[ERROR] Python virtual environment is not active"
    exit 1
fi

if ! python -c "import fastapi, uvicorn"; then
    echo "[ERROR] Python dependencies are missing"
    exit 1
fi

echo "[OK] Development environment is ready!"