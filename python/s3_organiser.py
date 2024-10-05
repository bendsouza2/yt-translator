"""Module for managing file storage in S3"""

import os

import boto3
from botocore.exceptions import ClientError

import utils

if (public_key := os.getenv("aws_public_key") is not None) and (
        secret_key := os.getenv("aws_secret_key") is not None):
    session = boto3.Session(
        aws_access_key_id=public_key,
        aws_secret_access_key=secret_key,
    )


class BucketSort:

    def __init__(
            self,
            bucket: str
    ):
        self.s3_client = boto3.client("s3")
        self.s3_resource = boto3.resource("s3")
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

    def move_file(self, file: str, current_directory: str, new_directory: str):
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

    def delete_file(self, path: str):
        """
        Delete a file from the S3 bucket
        :param path: the absolute path to the file to be deleted
        """
        self.s3_resource.Object(Bucket=self.s3_bucket, Key=path).delete()

