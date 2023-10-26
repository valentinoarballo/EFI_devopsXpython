#!/bin/bash
flask db init
flask db migrate -m "initial_migration"
flask db upgrade
gunicorn app:app --bind 0.0.0.0:5055 
