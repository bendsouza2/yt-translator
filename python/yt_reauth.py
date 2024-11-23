import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from python.constants import Paths


SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

creds = None
if os.path.exists(Paths.YT_TOKEN_PATH):
    creds = Credentials.from_authorized_user_file(Paths.YT_TOKEN_PATH, SCOPES)

if creds and creds.expired and creds.refresh_token:
    print(creds)
    creds.refresh(Request())

