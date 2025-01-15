import mimetypes
from typing import AsyncGenerator

import aioboto3
from aiohttp import ClientSession
from botocore.exceptions import NoCredentialsError
import os
from botocore.config import Config

CHUNK_SIZE = 1 * 1024 * 1024

config = Config(
    connect_timeout=10,
    read_timeout=30
)
bucket_name = os.getenv("S3_BUCKET_NAME")
region = os.getenv("S3_REGION")
access_key = os.getenv("S3_ACCESS_KEY")
secret_key = os.getenv("S3_SECRET_KEY")
endpoint_url = os.getenv("S3_ENDPOINT_URL")

if not all([bucket_name, region, access_key, secret_key]):
    raise RuntimeError("AWS S3 конфигурация отсутствует в переменных окружения")


class S3Service:
    def __init__(self, bucket_name: str, region: str, access_key: str,
                 secret_key: str, endpoint_url: str = None, config: Config = None):
        self.bucket_name = bucket_name
        self.region = region
        self.access_key = access_key
        self.secret_key = secret_key
        self.endpoint_url = endpoint_url
        self.config = config

    async def upload_file(self, file, file_name: str, folder: str = "") -> str:
        """
        Загружает файл в S3 и возвращает публичный URL.
        :param file: файл-объект
        :param file_name: желаемое имя файла (с расширением)
        :param folder: папка в S3, куда сохраняется файл
        """
        s3_path = f"{folder}/{file_name}" if folder else file_name
        session = aioboto3.Session()

        try:
            async with session.client(
                's3',
                region_name=self.region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                endpoint_url=self.endpoint_url,
            ) as s3_client:
                await s3_client.upload_fileobj(
                    Fileobj=file.file,
                    Bucket=self.bucket_name,
                    Key=s3_path,
                    ExtraArgs={"ACL": "public-read"}  # Делаем файл доступным публично
                )
            return s3_path
        except NoCredentialsError:
            raise RuntimeError("AWS credentials not found")
        except Exception as e:
            raise RuntimeError(f"Error during file upload: {str(e)}")

    async def delete_file(self, file_path: str):
        """Удаляет файл из S3."""
        session = aioboto3.Session()

        try:
            async with session.client(
                's3',
                region_name=self.region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                endpoint_url=self.endpoint_url,
            ) as s3_client:
                await s3_client.delete_object(Bucket=self.bucket_name, Key=file_path)
        except NoCredentialsError:
            raise RuntimeError("AWS credentials not found")

    async def get_file(self, file_key: str) -> AsyncGenerator[bytes, None]:
        """
        Асинхронно получает файл из S3 и возвращает его частями.
        """
        session = aioboto3.Session()

        async with session.client(
                's3',
                region_name=self.region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                endpoint_url=self.endpoint_url,
                config=self.config,
        ) as s3_client:
            try:
                # Узнаем размер файла
                head = await s3_client.head_object(Bucket=self.bucket_name, Key=file_key)
                content_length = head["ContentLength"]

                # Читаем файл кусками
                for offset in range(0, content_length, CHUNK_SIZE):
                    end = min(offset + CHUNK_SIZE - 1, content_length - 1)
                    response = await s3_client.get_object(
                        Bucket=self.bucket_name, Key=file_key, Range=f"bytes={offset}-{end}"
                    )

                    async with response["Body"] as stream:
                        yield await stream.read()
            except s3_client.exceptions.NoSuchKey:
                raise FileNotFoundError("File not found in S3")
            except NoCredentialsError:
                raise RuntimeError("AWS credentials not found")


async def get_s3_service() -> S3Service:
    return S3Service(bucket_name=bucket_name, region=region, access_key=access_key,
                     secret_key=secret_key, endpoint_url=endpoint_url, config=config)
