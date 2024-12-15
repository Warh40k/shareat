import mimetypes
import aioboto3
from botocore.exceptions import NoCredentialsError
import os

bucket_name = os.getenv("S3_BUCKET_NAME")
region = os.getenv("S3_REGION")
access_key = os.getenv("S3_ACCESS_KEY")
secret_key = os.getenv("S3_SECRET_KEY")
endpoint_url = os.getenv("S3_ENDPOINT_URL")

if not all([bucket_name, region, access_key, secret_key]):
    raise RuntimeError("AWS S3 конфигурация отсутствует в переменных окружения")


class S3Service:
    def __init__(self, bucket_name: str, region: str, access_key: str, secret_key: str, endpoint_url: str = None):
        self.bucket_name = bucket_name
        self.region = region
        self.access_key = access_key
        self.secret_key = secret_key
        self.endpoint_url = endpoint_url

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

    async def get_file(self, file_key: str) -> tuple:
        """
        Получает файл из S3 и возвращает поток и тип контента.
        """
        session = aioboto3.Session()

        try:
            async with session.client(
                's3',
                region_name=self.region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                endpoint_url=self.endpoint_url,
            ) as s3_client:
                response = await s3_client.get_object(Bucket=self.bucket_name, Key=file_key)
                file_stream = response['Body']
                content_type, _ = mimetypes.guess_type(file_key)
                if not content_type:
                    content_type = 'application/octet-stream'  # Фолбэк на универсальный тип
                return file_stream, content_type
        except s3_client.exceptions.NoSuchKey:
            raise FileNotFoundError("File not found in S3")
        except NoCredentialsError:
            raise RuntimeError("AWS credentials not found")


async def get_s3_service() -> S3Service:
    return S3Service(bucket_name=bucket_name, region=region, access_key=access_key,
                     secret_key=secret_key, endpoint_url=endpoint_url)
