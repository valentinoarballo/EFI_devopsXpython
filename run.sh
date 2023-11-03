#!/bin/bash

sleep 15
echo "RUNNING > db init"
flask db init
sleep 15

echo "RUNNING > db migrate -m initial_migration"
flask db migrate -m "initial_migration"
sleep 15

echo "RUNNING > db upgrade"
flask db upgrade
sleep 15

gunicorn app:app --bind 0.0.0.0:5055 --reload
