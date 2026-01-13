#!/usr/bin/env bash
set -euo pipefail

echo "Applying "
alembic -c src/infrastructure/config/migrations/alembic.ini upgrade head

echo "[entrypoint] Migraciones aplicadas. Iniciando Uvicorn..."
exec uvicorn app:app --host 0.0.0.0 --port 8000
