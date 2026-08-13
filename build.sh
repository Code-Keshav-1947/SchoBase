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
