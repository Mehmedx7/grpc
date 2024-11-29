#!/bin/sh
echo "Pre script running"
python /app/manage.py makemigrations
python /app/manage.py migrate
python /app/manage.py makemigrations ecomm
python /app/manage.py migrate ecomm
