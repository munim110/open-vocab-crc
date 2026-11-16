# Shared environment, sourced by every script in this directory.
# Resolves the repository root and a Python interpreter so the scripts run
# correctly no matter what the working directory is.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PYTHON:-$ROOT/.venv/bin/python}"
[ -x "$PY" ] || PY="$(command -v python3)"
export PYTHONUNBUFFERED=1
mkdir -p "$ROOT/logs"
