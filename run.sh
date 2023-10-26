#!/bin/bash

echo "RUNNING > db init"
flask db init
sleep 10

echo "RUNNING > db migrate -m initial_migration"
flask db migrate -m "initial_migration"
sleep 10

echo "RUNNING > db upgrade"
flask db upgrade
sleep 10

gunicorn app:app --bind 0.0.0.0:5055 --reload
