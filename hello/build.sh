#!/usr/bin/env bash
# Exit on error
set -o errexit

# 1. Dependencies install karein
pip install -r requirements.txt

# 2. Hello folder ke andar jayein jahan manage.py hai


# 3. Django commands chalayein
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

export DJANGO_SETTINGS_MODULE=hello.settings

