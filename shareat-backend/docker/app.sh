#!/bin/bash

alembic upgrade head

python3 actions/create_superuser.py

poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload