#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
python << 'PYEOF'
import socket, os, sys, time
from urllib.parse import urlparse

database_url = os.environ.get('DATABASE_URL', '')
if database_url:
    parsed = urlparse(database_url)
    host = parsed.hostname or 'db'
    port = parsed.port or 5432
else:
    host = 'db'
    port = 5432

for i in range(30):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((host, port))
        s.close()
        print(f"PostgreSQL is ready at {host}:{port}")
        sys.exit(0)
    except Exception:
        print(f"Attempt {i+1}: waiting for {host}:{port}...")
        time.sleep(2)

print("ERROR: Could not connect to PostgreSQL after 30 attempts", file=sys.stderr)
sys.exit(1)
PYEOF

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Checking if database needs seeding..."
LOCATION_COUNT=$(python manage.py shell -c "from audit.models import Location; print(Location.objects.count())")
if [ "$LOCATION_COUNT" -eq "0" ]; then
  echo "Database is empty. Loading seed data..."
  python manage.py seed_data
  python manage.py setup_roles
  echo "Seed data and roles loaded successfully."
else
  echo "Database already contains data. Skipping seed."
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec "$@"
