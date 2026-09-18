#!/bin/sh

set -e

# Run migrations if needed
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files if needed (usually for production, but good to have)
if [ "$SYSTEM_ENV" = "PRODUCTION" ] || [ "$SYSTEM_ENV" = "STAGING" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput --clear
fi

exec "$@"
