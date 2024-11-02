#!/bin/bash

# Выполнение миграций Alembic
alembic upgrade head

# Создание суперпользователя
python actions/create_superuser.py

# Запуск приложения Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload