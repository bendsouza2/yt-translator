"""Module for connecting to YouTube and uploading videos"""
import os
import json
from typing import Optional, Sequence, Dict, Any, List
from dotenv import load_dotenv

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

from python.constants import EnvVariables, BUCKET_NAME
from python.s3_organiser import BucketSort
from python import utils


load_dotenv()


class YTConnector:
    """Class for connecting to YouTube via its API"""

    def __init__(
            self,
            credentials_path: Optional[str] = None,
            credentials_env: bool = False,
            cloud_storage: bool = False,
    ):
        """
        Initialise a YTConnector object
        :param credentials_path: Optional. The absolute path to the credentials
        :param credentials_env: If true, the credentials will be loaded from the 'YOUTUBE_CREDENTIALS' env variable
        :param cloud_storage: True if the videos and related content are stored in S3, False otherwise
        """
        self.credentials_path = credentials_path
        self.credentials_env = credentials_env  # type: ignore[assignment]
        self.cloud_storage = cloud_storage
        self.credentials = self.get_yt_credentials()
        self.youtube_client = self.build_yt_client()

    @property
    def credentials_env(self) -> None | Dict[str, str]:
        """
        Gets the environment variable for YouTube API credentials
        :return: A dictionary containing the YouTube API credentials if available, or None if not set.
        """
        return self._credentials_env

    @credentials_env.setter
    def credentials_env(self, credentials_env):
        """
        Set the self.credentials_env attribute
        :param credentials_env: A flag indicating whether to set the credentials. If False, sets the attribute to None.
        Otherwise, loads the credentials from the env variable
        """
        if credentials_env is False:
            self._credentials_env = None
        else:
            creds = os.getenv(EnvVariables.YOUTUBE_CREDENTIALS)
            self._credentials_env = json.loads(creds)

    def get_yt_credentials(self) -> Credentials:
        """
        Get the credentials required to connect to YouTube. Will use the credentials stored in the environment if
        available, else will use the path to the credentials file if provided
        :return: The youtube credentials
        """
        if self.credentials_path is None and self.credentials_env is None:
            raise ValueError(f"Could not connect to the YouTube API - you must provide the credentials either via the "
                             f"credentials_path arg or the credentials_env arg")
        elif self.credentials_env is not None:
            service = Credentials.from_authorized_user_info(self.credentials_env)
            return service
        else:
            return self.build_creds_from_file()

    def build_creds_from_file(self) -> Credentials:
        """
        Builds the required youtube credentials from a given token file
        :return: a dict containing the creds
        """
        if not os.path.exists(self.credentials_path):  # type: ignore[arg-type]
            raise FileNotFoundError(f"Credentials file could not be found: {self.credentials_path} is not a valid path")

        with open(self.credentials_path, "r") as token_file:  # type: ignore[arg-type]
            cred_data = json.load(token_file)

        creds = Credentials(
            token=cred_data['token'],
            refresh_token=cred_data['refresh_token'],
            token_uri=cred_data['token_uri'],
            client_id=cred_data['client_id'],
            client_secret=cred_data['client_secret'],
            scopes=cred_data['scopes']
        )

        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

        return creds

    def build_yt_client(self):
        """Build the youtube client from given credentials"""
        youtube = build("youtube", "v3", credentials=self.credentials)
        return youtube

    def upload_youtube_short(
            self,
            video_path: str,
            title: str,
            description: str,
            tags: Optional[Sequence] = None,
            category_id: int = 27,
            private_video: bool = False,
            made_for_kids: bool = False,
    ) -> Dict:
        """
        Upload a video to youtube shorts
        :param video_path: the absolute path to the video to upload
        :param title: the title to give to the video
        :param description: the description to add for the video
        :param tags: tags to add for the video
        :param category_id: the content category that the video belongs to
        :param private_video: if the video should be private, defaults to False
        :param made_for_kids: if the video is target at kids, defaults to False,
        :return: a dictionary with the response from the API
        """
        if self.cloud_storage is True:
            s3_bucket = BucketSort(bucket=BUCKET_NAME)
            video_bytes = s3_bucket.get_object_from_s3(s3_key=video_path)
            video = utils.write_bytes_to_local_temp_file(bytes_object=video_bytes, suffix="mp4", delete_file=False)
        else:
            video = video_path
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video file not found: {video_path}")

        status = "private" if private_video is True else "public"
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags or [],
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': status,
                'selfDeclaredMadeForKids': made_for_kids,
            }
        }

        media = MediaFileUpload(
            video,
            mimetype='video/*',
            resumable=True,
            chunksize=1024 * 1024  # 1MB chunks
        )

        insert_request = self.youtube_client.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = insert_request.next_chunk()

        video_id = response['id']
        video_url = f"https://youtube.com/shorts/{video_id}"

        if self.cloud_storage is True:
            utils.remove_temp_file(video)

        print(f"Upload Complete! Short URL: {video_url}")
        return response

    def delete_youtube_short(self, video_id: str) -> Dict[str, str]:
        """
        Delete a youtube video
        :param video_id: the ID of the video to be deleted
        :return: a status message confirming the video deletion
        """
        confirmation = input(
            f"WARNING: You are about to delete the video with ID {video_id}. This action is irreversible. "
            f"Are you sure you want to proceed? (y/n): ").strip().lower()

        if confirmation != "y":
            return {"status": "cancelled", "message": "Video deletion cancelled by the user."}

        delete_request = self.youtube_client.videos().delete(id=video_id)
        delete_request.execute()

        return {"status": "success", "message": f"Video with ID {video_id} deleted successfully."}

    def list_yt_subscriptions(self) -> Dict[str, Any]:
        """
        List subscriptions
        :return: a dictionary with the metadata for the subscriptions
        """
        request = self.youtube_client.subscriptions().list(
            part="snippet,contentDetails",
            mine=True
        )
        response = request.execute()
        return response

    def list_available_channels(self) -> List[Dict[str, str]]:
        """
        List the available channels associated with the authorised account
        :return: a dictionary with the metadata for each channel
        """
        channel_response = self.youtube_client.channels().list(
            part="snippet,contentDetails",
            mine=True
        ).execute()
        channels = [
            {
                'id': channel['id'],
                'title': channel['snippet']['title'],
                'description': channel['snippet'].get('description', '')
            }
            for channel in channel_response.get('items', [])
        ]

        return channels

    def list_youtube_uploads(self, channel_id: str, max_results: int = 50) -> Dict[str, Dict[str, str]]:
        """
        Get the details of the videos uploaded to a youtube channel
        :param channel_id: the ID for the channel to get the uploads for
        :param max_results: the number of video uploads to get the data for
        :return: A dictionary with the video_id as the key and a nested dictionary with the video title, description
        and thumbnail url as the value
        """
        response = self.youtube_client.search().list(
            part="id,snippet",
            channelId=channel_id,
            maxResults=max_results,
            type="video"
        ).execute()

        video_dict = {}
        for item in response.get("items", []):

            video_id = item['id']['videoId']
            title = item['snippet']['title']
            description = item['snippet']['description']
            thumbnail_url = item['snippet']['thumbnails']['high']['url']
            published_at = item['snippet']['publishedAt']

            video_dict[video_id] = {
                "title": title,
                "description": description,
                "thumbnail_url": thumbnail_url,
                "published_at": published_at,
            }

        return video_dict
