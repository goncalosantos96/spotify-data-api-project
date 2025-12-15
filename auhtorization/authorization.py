import os
import requests
from typing import Dict

# Read Spotify token endpoint from environment variables
SPOTIFY_URL_TOKEN = os.getenv('SPOTIFY_URL_TOKEN')

# Read Spotify API credentials securely from environment variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


def get_token(url_token: str, payload: dict, headers: dict):
    # Request an OAuth access token from Spotify
    try:
        response = requests.post(url_token, data=payload, headers=headers)

        # Raises an exception for HTTP errors (4xx / 5xx)
        response.raise_for_status()

        # Convert response body to JSON
        data = response.json()

        # Extract access token from response
        access_token = data.get("access_token")

        # Defensive check in case token is missing
        if not access_token:
            print("Error: No token provided")
            print(f"Response: {data}")
            return None

        return access_token

    except Exception:
        # Log minimal error information for debugging
        print("Status code:", response.status_code)
        print("Response:", response.text[:200])
        return None


def get_auth_request() -> Dict:
    # Payload required by Spotify Client Credentials flow
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }

    # Header specifying form-encoded request body
    headers = {
        'Content-type': 'application/x-www-form-urlencoded'
    }

    # Retrieve access token
    token = get_token(SPOTIFY_URL_TOKEN, payload, headers)

    # Attach Bearer token to Authorization header
    headers['Authorization'] = f'Bearer {token}'

    return headers
