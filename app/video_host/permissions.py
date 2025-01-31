"""Module for managing permissions and authentication for the app"""
import os

import dotenv
from rest_framework.permissions import BasePermission

dotenv.load_dotenv()


class HasValidApiKey(BasePermission):
    """Class to check that there is a valid API key"""
    def has_permission(self, request, view) -> bool:
        """
        Checks whether the request contains a valid API key in its headers.

        This method checks the 'X-API-KEY' header in the request and compares it against the expected API key
        stored in the environment variable. If the keys match, permission is granted; otherwise, access is denied.

        :param request: The HTTP request object containing headers with the API key.
        :param view: The view for which permission is being checked.
        :return: True if the API key in the request headers matches the expected API key, False otherwise.
        """
        api_key = request.headers.get("X-API-KEY")
        return api_key == os.getenv("EXPECTED_API_KEY")
