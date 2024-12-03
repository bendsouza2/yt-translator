"""This module can be used to authenticate the app with your Google Account"""
import os

from google_auth_oauthlib.flow import InstalledAppFlow

from constants import Paths, EnvVariables
import base_config

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

flow = InstalledAppFlow.from_client_secrets_file(
    f"{base_config.BASE_DIR}/{Paths.GOOGLE_CREDS_PATH}", SCOPES
)

creds = flow.run_local_server(
    port=8080,
    prompt='consent',
    authorization_prompt_message='Please authorize access to YouTube',
    authorization_code_message='Enter the authorization code from the link above'
)

if not creds.refresh_token:
    flow.oauth2session.params['access_type'] = 'offline'
    flow.oauth2session.params['prompt'] = 'consent'
    creds = flow.run_local_server(
        port=8080,
        prompt='consent'
    )

print("Access Token:", creds.token)
print("Refresh Token:", creds.refresh_token)
print("Token URI:", creds.token_uri)
print("Client ID:", creds.client_id)
print("Client Secret:", creds.client_secret)


with open(f"{base_config.BASE_DIR}/{Paths.YT_TOKEN_PATH}", "w") as token_file:
    token_file.write(creds.to_json())

new_env_line = f'{EnvVariables.YOUTUBE_CREDENTIALS}={creds.to_json()}\n'

if os.path.exists(f"{base_config.BASE_DIR}/{Paths.PYTHON_ENV_FILE}"):
    with open(f"{base_config.BASE_DIR}/{Paths.PYTHON_ENV_FILE}", "r") as file:
        lines = file.readlines()

    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"{EnvVariables.YOUTUBE_CREDENTIALS}="):
            lines[i] = new_env_line
            updated = True
            break

    if not updated:
        lines.append(new_env_line)

    with open(f"{base_config.BASE_DIR}/{Paths.PYTHON_ENV_FILE}", "w") as file:
        file.writelines(lines)
else:
    with open(f"{base_config.BASE_DIR}/{Paths.PYTHON_ENV_FILE}", "w") as file:
        file.write(new_env_line)
