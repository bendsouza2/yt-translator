"""Module for connecting to YouTube and uploading videos"""
import os
import json
from typing import Optional, Sequence, Dict, Any
from dotenv import load_dotenv

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload


load_dotenv()


class YTConnector:
    """Class for connecting to YouTube via its API"""

    def __init__(
            self,
            credentials_path: Optional[str] = None,
            credentials_env: bool = False,
    ):
        """
        Initialise a YTConnector object
        :param credentials_path: Optional. The absolute path to the credentials
        :param credentials_env: If true, the credentials will be loaded from the 'YOUTUBE_CREDENTIALS' env variable
        """
        self.credentials_path = credentials_path
        self.credentials_env = credentials_env  # type: ignore [assignment]
        self.credentials = self.get_yt_credentials()
        self.youtube_client = self.build_yt_client()

    @property
    def credentials_env(self) -> None | Dict[str, str]:
        """Gets the environment variable for YouTube API credentials"""
        return self._credentials_env

    @credentials_env.setter
    def credentials_env(self, credentials_env):
        """
        Set the self.credentials_env attribute
        """
        if credentials_env is False:
            self._credentials_env = None
        else:
            creds = os.getenv("YOUTUBE_CREDENTIALS")
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
        if not os.path.exists(self.credentials_path):  # type: ignore [arg-type]
            raise FileNotFoundError(f"Credentials file could not be found: {self.credentials_path} is not a valid path")

        with open(self.credentials_path, "r") as token_file:  # type: ignore [arg-type]
            cred_data = json.load(token_file)

        creds = Credentials(
            token=cred_data['token'],
            refresh_token=cred_data['refresh_token'],
            token_uri=cred_data['token_uri'],
            client_id=cred_data['client_id'],
            client_secret=cred_data['client_secret'],
            scopes=cred_data['scopes']
        )

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
            video_path,
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

        print(f"Upload Complete! Short URL: {video_url}")
        return response

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

    def list_available_channels(self):
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
