#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
until python -c "
import socket, os, sys
host = os.environ.get('DB_HOST', 'db')
port = int(os.environ.get('DB_PORT', '5432'))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))
    s.close()
    sys.exit(0)
except:
    sys.exit(1)
" 2>/dev/null; do
  sleep 1
done

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
