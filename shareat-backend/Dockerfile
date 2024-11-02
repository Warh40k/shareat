# Используем официальный образ Python
FROM python:3.12-slim

# set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Копируем файлы конфигурации Poetry
COPY pyproject.toml poetry.lock* ./

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Устанавливаем зависимости в системную среду, чтобы не использовать poetry run
RUN poetry config virtualenvs.create false && poetry install --no-root --without dev

# Копируем оставшиеся файлы проекта
COPY . .

# Открываем порт (если нужно, для работы сервера)
EXPOSE 8000

# Команда запуска (можно заменить на запуск скрипта напрямую)
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]