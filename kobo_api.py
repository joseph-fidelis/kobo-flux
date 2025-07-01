"""
This module contains functions to interact with the Kobo API.
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

class KoboAPI:
    """
    API manager for interacting with KOBO
    """
    def __init__(self):
        self.base_url = os.getenv('BASE_URL')
        self.token = os.getenv('API_TOKEN')

    def post_with_auth(self, url: str, json_body: dict) -> requests.Response:
        """
        Send a POST request with a JSON body and Authorization header.
        The token is loaded from the environment variable 'API_TOKEN'.
        """
        token = os.getenv('API_TOKEN')
        base_url = os.getenv('BASE_URL')
        url = f"{base_url}{url}"
        if not token:
            raise ValueError("API_TOKEN not set in environment variables.")
        if not base_url:
            raise ValueError("BASE_URL not set in environment variables.")
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=json_body, headers=headers, timeout=20)
        response.raise_for_status()
        return response

    def _get_with_auth(self, url: str) -> requests.Response:
        """
        Send a GET request with an Authorization header.
        The token is loaded from the environment variable 'API_TOKEN'.
        """
        token = os.getenv('API_TOKEN')
        base_url = os.getenv('BASE_URL')    
        url = f"{base_url}{url}"
        if not token:
            raise ValueError("API_TOKEN not set in environment variables.")
        if not base_url:
            raise ValueError("BASE_URL not set in environment variables.")
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        return response


    def get_forms(self) -> list[dict]:
        """
        Get a list of all forms from the Kobo API.
        """
        url = "/forms"
        response = self._get_with_auth(url)
        return response.json()