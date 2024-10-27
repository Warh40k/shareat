# Используем официальный образ Python
FROM python:3.12-slim

# set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Копируем файлы конфигурации Poetry
COPY pyproject.toml poetry.lock* ./

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry && poetry install --no-root --without dev && rm -rf ~/.cache/pip

# Копируем оставшиеся файлы проекта
COPY . .

# Запускаем приложение
# CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
