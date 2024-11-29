import os
from typing import Dict

import MySQLdb


def write_to_db(video_details: Dict[str, str]) -> None:
    """
    Writes video metadata to a MySQL database using mysqlclient (MySQLdb).
    :param video_details: Dictionary containing the data to write to the DB
    """
    connection = None
    try:
        connection = MySQLdb.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASSWORD"),
            db=os.getenv("DB_NAME"),
        )
        cursor = connection.cursor()

        sql_query = """
        INSERT INTO videos (video_id, word, sentence, translated_sentence, title, description, upload_time, thumbnail_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            word = VALUES(word),
            sentence = VALUES(sentence),
            translated_sentence = VALUES(translated_sentence),
            title = VALUES(title),
            description = VALUES(description),
            upload_time = VALUES(upload_time),
            thumbnail_url = VALUES(thumbnail_url);
        """
        cursor.execute(
            sql_query,
            (
                video_details["video_id"],
                video_details["word"],
                video_details["sentence"],
                video_details["translated_sentence"],
                video_details["title"],
                video_details["description"],
                video_details["upload_time"],
                video_details["thumbnail_url"],
            ),
        )

        connection.commit()

    except MySQLdb.Error as e:
        print(f"Error while interacting with the database: {e}")
        raise

    finally:
        if connection is not None:
            connection.close()
