import boto3
import botocore
from maaslogger import base_logger
from simple_settings import settings

logger = base_logger.get_logger(__name__)


class S3CloudManager:

    def __init__(self, bucket):
        self.bucket_name = bucket
        boto3.set_stream_logger(name='botocore')
        session = boto3.session.Session()
        self.s3_client = session.client(
            's3',
            aws_access_key_id=settings.S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.S3_ACCESS_KEY_SECRET,
            endpoint_url=settings.S3_ENDPOINT_URL,
            config=botocore.client.Config(signature_version='s3'),
        )

    def upload(self, file_name, object_name=None):
        try:
            self.s3_client.upload_file(file_name,
                                       self.bucket_name,
                                       object_name)
        except Exception:
            return False
        return True

    def delete(self, file_name, object_name=None):
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_name)
        except Exception as e:
            logger.error(
                'There was a problem to upload {}, {}'
                .format(file_name, e.__cause__)
            )
            return False
        return True

    def get_file(self, file_name, object_name=None):
        if object_name is None:
            object_name = file_name
        try:
            with open(file_name, 'wb') as f:
                self.s3_client.download_file(
                    self.bucket_name,
                    object_name,
                    f)
        except Exception:
            return False
        return True

    def get_object(self,
                   file_name,
                   object_name=None):
        if object_name is None:
            object_name = file_name
        try:
            with open(file_name, 'wb') as f:
                self.s3_client.download_fileobj(
                    self.bucket_name,
                    object_name,
                    f)
        except Exception:
            return False
        return True
