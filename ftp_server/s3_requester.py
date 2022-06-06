import boto3


class S3Requester:
    def __init__(self, ak: str, sk: str, bucket: str) -> None:
        self.bucket = bucket
        self.client = boto3.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net',
            aws_access_key_id=ak,
            aws_secret_access_key=sk,
        )

    def upload_object(self, filename: str, obj):
        self.client.upload_fileobj(obj, self.bucket, filename)
