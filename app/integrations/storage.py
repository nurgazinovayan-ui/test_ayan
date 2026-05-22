import os
import uuid
import cloudinary.uploader
import boto3
from app.core.config import get_settings

settings = get_settings()


def upload_image(file_path: str) -> str:
    if settings.cloud_storage_provider == 's3':
        key = f"drafts/{uuid.uuid4().hex}.png"
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.s3_access_key_id,
            aws_secret_access_key=settings.s3_secret_access_key,
            region_name=settings.s3_region,
        )
        s3.upload_file(file_path, settings.s3_bucket_name, key, ExtraArgs={'ContentType': 'image/png'})
        return f"https://{settings.s3_bucket_name}.s3.{settings.s3_region}.amazonaws.com/{key}"

    cloudinary.config(
        cloud_name=settings.cloudinary_cloud_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
    )
    result = cloudinary.uploader.upload(file_path, folder='insta-agent')
    return result['secure_url']
