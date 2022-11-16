#!/bin/sh

while ! nc -z mysql 3306 ; do
    echo "Waiting for the MySQL Server to spin up...."
    sleep 3
done

python manage.py runserver 0.0.0.0:8000