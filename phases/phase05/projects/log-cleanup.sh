#!/bin/bash
# log-cleanup.sh – Rotate, compress, and clean old logs

set -e

# Configuration
LOG_DIR="/var/log"
ARCHIVE_DIR="/var/log/archive"
DAYS_TO_KEEP=7
COMPRESSION="gzip"
MAX_DISK_USAGE=80
ADMIN_EMAIL="admin@example.com"

# Functions
send_alert() {
    local message="$1"
    echo "$message" | mail -s "Log Cleanup Alert" "$ADMIN_EMAIL"
}

# Create archive directory if missing
mkdir -p "$ARCHIVE_DIR"

# Compress logs older than 1 day
echo "Compressing logs older than 1 day..."
find "$LOG_DIR" -name "*.log" -type f -mtime +1 -exec $COMPRESSION {} \;

# Move compressed logs to archive
echo "Archiving old logs..."
find "$LOG_DIR" -name "*.gz" -type f -mtime +$DAYS_TO_KEEP -exec mv {} "$ARCHIVE_DIR" \;

# Delete logs older than 30 days from archive
echo "Deleting archived logs older than 30 days..."
find "$ARCHIVE_DIR" -name "*.gz" -type f -mtime +30 -delete

# Check disk usage
disk_usage=$(df -h "$LOG_DIR" | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$disk_usage" -gt "$MAX_DISK_USAGE" ]; then
    send_alert "WARNING: Log directory is $disk_usage% full!"
fi

echo "Log cleanup complete."