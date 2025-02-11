"""Module for implementing the AWS Lambda logic"""
import os
import logging
import traceback
from typing import Dict, Any

import MySQLdb

from python.main import process_video_and_upload

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Lambda entry point to process video, upload to YouTube, and write metadata to db.
    :param event: The event data passed to the lambda function
    :param context: The context object providing runtime information about the Lambda execution, such as the function
    name, request ID and remaining execution time.
    :returns: A dictionary with a `statusCode` and `body` containing the result of the Lambda execution.
    """
    try:
        required_env_vars = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if len(missing_vars) > 0:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

        video_details = process_video_and_upload(write_to_rds=True)

        return {
            "statusCode": 200,
            "body": {
                "message": "Video processed and uploaded successfully",
                "video_details": video_details,
            },
        }

    except EnvironmentError:
        logger.error(f"Environment Error: {traceback.format_exc()}")
        return {
            "statusCode": 400,
            "body": {
                "message": "Missing required environment variables",
                "error": traceback.format_exc(),
            },
        }

    except MySQLdb.Error:
        logger.error(f"MySQL Error: {traceback.format_exc()}")
        return {
            "statusCode": 500,
            "body": {
                "message": "Database error occurred while processing video",
                "error": traceback.format_exc(),
            },
        }

    except ValueError:
        logger.error(f"Value Error: {traceback.format_exc()}")
        return {
            "statusCode": 400,
            "body": {
                "message": "Invalid data error occurred during processing",
                "error": traceback.format_exc(),
            },
        }

