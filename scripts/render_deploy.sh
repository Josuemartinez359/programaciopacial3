#!/usr/bin/env bash
set -euo pipefail

echo "[render_deploy] starting deploy hook"

# Decide where manage.py lives. Prefer 'actividad 1' directory if present.
if [ -f "manage.py" ]; then
  echo "[render_deploy] found manage.py in repo root"
elif [ -f "actividad 1/manage.py" ]; then
  echo "[render_deploy] found manage.py in actividad 1 — changing directory"
  cd "actividad 1"
else
  echo "[render_deploy] ERROR: manage.py not found in repo root or actividad 1"
  exit 1
fi

echo "[render_deploy] Running migrations and collectstatic"
python -m pip install --upgrade pip || true
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "[render_deploy] completed"
