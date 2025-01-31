"""Module for establishing and handling MySQL DB connection"""
import os
import requests
from typing import Dict

import MySQLdb
import dotenv

from python import utils

dotenv.load_dotenv()


def write_to_db(video_details: Dict[str, str]) -> requests.Response:
    """
    Writes video metadata to a MySQL database by calling an API endpoint, which writes the data to the DB.
    :param video_details: Dictionary containing the data to write to the DB
    """

    base_url = os.getenv('API_BASE_URL')
    if base_url is None:
        raise ValueError("No 'API_BASE_URL' env variable could be found")
    base_url = utils.remove_trailing_slash(base_url)
    api_url = f"{base_url}/today/videos/write-to-db/"
    api_key = os.getenv("EXPECTED_API_KEY")

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": api_key,
    }

    response = requests.post(api_url, json=video_details, headers=headers)
    response.raise_for_status()

    return response

