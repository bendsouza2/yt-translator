import os
import logging
import traceback

import MySQLdb

from python.main import process_video_and_upload
from python.db_handler import write_to_db

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler():
    """
    Lambda entry point to process video, upload to YouTube, and write metadata to db.
    """
    try:
        required_env_vars = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

        video_details = process_video_and_upload(db_write_function=write_to_db)

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

