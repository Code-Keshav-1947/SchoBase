#!/usr/bin/env bash
# Exit on error
set -o errexit

# 1. Dependencies install karein
pip install -r requirements.txt

# 2. Hello folder ke andar jayein jahan manage.py hai
cd hello

# 3. Django commands chalayein
python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate

python -c "
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='boss').exists():
    User.objects.create_superuser('boss', 'boss@example.com', 'BossPass123')
    print('Superuser boss created successfully!')
"