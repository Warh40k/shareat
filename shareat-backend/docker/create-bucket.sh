#!/bin/sh

set -e

# Добавляем alias для подключения к MinIO
mc alias set local http://localhost:9000 admin admin123

# Проверяем, существует ли бакет
if mc ls local/shareat-bucket >/dev/null 2>&1; then
  echo "Bucket 'shareat-bucket' already exists."
else
  # Создаем бакет
  mc mb local/shareat-bucket
  echo "Bucket 'shareat-bucket' created successfully."
fi
