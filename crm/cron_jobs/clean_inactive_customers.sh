#!bin/bash

# 1. Use Django's manage.py to execute a python command 
# that deletes customers with no orders since a year ago
PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
LOG_FILE="/tmp/customer_cleanup_log.txt"

cd "$PROJECT_DIR" || exit 1

DELETED_COUNT=$(python manage.py shell <<EOF
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(orders__isnull=True,
created_at__lt=one_year_ago)
count = qs.count
qs.delete()
print(count)
EOF
)

echo "$(date '+%Y-%m-%d %H:%M:%S')" - Deleted customers: $DELETED_COUNT" >> "$LOG_FILE"