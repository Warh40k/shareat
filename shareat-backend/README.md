##Docker 
Крч если хотите запустить в докере очевидно епта че делать.
Будет выполнено создание бд с созданием админа.

Ну че надо отредактируйте.

##Локально
 Если хотите у себя запустить:
 Загрузите все нужное:
 ```
 pip install poetry

 poetry install
 ```
Проведите миграцию:
```
alembic upgrade head
```
Хотите создать админа?
```
python actions\create_superuser.py
```

Не забудьте добавить/изменить переменные среды: .env

Запустите в доцкере s3:
```
docker run -p 9000:9000 -p 9001:9001 \
  -e "MINIO_ROOT_USER=admin" \
  -e "MINIO_ROOT_PASSWORD=admin123" \
  quay.io/minio/minio server /data --console-address ":9001"
```

Ну и запуск говна (fastapi приложения):
```
uvicorn main:app --reload
```