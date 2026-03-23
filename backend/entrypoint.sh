#!/bin/sh
set -e

echo "Running database migrations..."
python -m src.db.migrate

echo "Starting application..."
exec "$@"
