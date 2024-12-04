"""Module for managing file storage in S3"""

import os
import dotenv
from typing import Union, IO

import boto3
from botocore.exceptions import ClientError

from python import utils

dotenv.load_dotenv()

if utils.is_running_on_aws() is True:
    session = boto3.Session()
elif (public_key := os.getenv("AWS_PUBLIC_KEY") is not None) and (
        secret_key := os.getenv("AWS_SECRET_KEY") is not None):
    session = boto3.Session(
        aws_access_key_id=public_key,
        aws_secret_access_key=secret_key,
    )
elif os.getenv("AWS_PROFILE_NAME") is not None:
    session = boto3.Session(
        profile_name=os.getenv("AWS_PROFILE_NAME")
    )


class BucketSort:
    """
    Class for reading and writing to S3
    """

    def __init__(
            self,
            bucket: str
    ):
        self.s3_client = session.client("s3")
        self.s3_resource = session.resource("s3")
        self.s3_bucket = bucket
        self.bucket_resource = self.s3_resource.Bucket(self.s3_bucket)

    def check_file_exists(self, path_to_check: str, filename: str) -> bool:
        """
        Check that a file exists in the S3 bucket
        :param path_to_check: The path to the directory the file should exist in
        :param filename: The name of the file to check for
        :return: True if the file exists, False if not
        """
        try:
            path_to_check = utils.remove_trailing_slash(path_to_check)
            s3_file = "/".join([path_to_check, filename])
            self.s3_client.head_object(Bucket=self.s3_bucket, Key=s3_file)
            return True
        except ClientError:
            return False

    def move_file(self, file: str, current_directory: str, new_directory: str) -> str:
        """
        Move files between directories within an S3 bucket
        :param file: The name of the file to move
        :param current_directory: The absolute path to the directory the file is stored in
        :param new_directory: The absolute path to the directory for the file to be moved to
        """
        new_path = "/".join([new_directory, file])
        copy_source = {
            "Bucket": self.s3_bucket,
            "Key": current_directory
        }
        self.bucket_resource.copy(CopySource=copy_source, Key=new_path)
        return new_path

    def delete_file(self, path: str) -> None:
        """
        Delete a file from the S3 bucket
        :param path: the absolute path to the file to be deleted
        """
        self.s3_resource.Object(Bucket=self.s3_bucket, Key=path).delete()

    def get_object_from_s3(self, s3_key: str) -> bytes:
        """
        Fetch the content of an object from the S3 bucket.
        :param s3_key: The key of the file in the S3 bucket
        :return: The content of the file as bytes
        """
        response = self.s3_client.get_object(Bucket=self.s3_bucket, Key=s3_key)
        return response['Body'].read()

    def push_file_to_s3(self, file_path: str, s3_key: str) -> str:
        """
        Upload a file to the S3 bucket.
        :param file_path: The local file path to the file to be uploaded.
        :param s3_key: The key (path and name) for the file in the S3 bucket.
        :return: The bucket path that the file is written to.
        """
        try:
            self.s3_client.upload_file(file_path, self.s3_bucket, s3_key)
            print(f"Successfully uploaded {file_path} to {self.s3_bucket}/{s3_key}")
            return s3_key
        except ClientError as e:
            print(f"Failed to upload {file_path} to {self.s3_bucket}/{s3_key}. Error: {e}")
            raise

    def push_object_to_s3(self, file: Union[str, bytes, IO], s3_key: str) -> str:
        """
        Upload an in-memory object to the S3 bucket.
        :param file: The content to upload. Can be a string, bytes, or a file-like object.
        :param s3_key: The key (path and name) for the file in the S3 bucket.
        :return: The S3 key of the uploaded object.
        """
        if isinstance(file, str):
            file = file.encode("utf-8")
        self.bucket_resource.put_object(Body=file, Key=s3_key)
        return s3_key

