from google_auth_oauthlib.flow import InstalledAppFlow

from constants import Paths

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

flow = InstalledAppFlow.from_client_secrets_file(
    Paths.GOOGLE_CREDS_PATH, SCOPES
)

creds = flow.run_local_server(port=8080)

print("Access Token:", creds.token)
print("Refresh Token:", creds.refresh_token)
print("Token URI:", creds.token_uri)
print("Client ID:", creds.client_id)
print("Client Secret:", creds.client_secret)

with open(Paths.YT_TOKEN_PATH, "w") as token_file:
    token_file.write(creds.to_json())
