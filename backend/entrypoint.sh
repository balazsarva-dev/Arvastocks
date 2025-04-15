#!/bin/bash

set -e

log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Set the PORT variable from the environment
PORT=${PORT:-5000}

# Start cron service
/usr/sbin/cron -f &

# Start the application using Gunicorn
log "Starting the application using Gunicorn..."
exec gunicorn app:app --bind 0.0.0.0:$PORT
if [ $? -ne 0 ]; then
  log "Gunicorn failed to start. Exiting."
  exit 1
fi