from dotenv import load_dotenv
import os
import requests

# Load the .env file
load_dotenv()

# Load the .env variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
SPOTIFY_URL_TOKEN = os.getenv('SPOTIFY_URL_TOKEN')
SPOTIFY_ARTISTS_ENDPOINT = os.getenv('')
genero = 'rock'
limit = 50
offset = 0
url = f'https://api.spotify.com/v1/search?q=genre:"{genero}"&type=artist&limit={limit}&offset={offset}'

payload = {

    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'client_credentials'
}

headers = {

    'Content-type': 'application/x-www-form-urlencoded'
}



response = requests.post(SPOTIFY_URL_TOKEN, payload, headers)
print(response.json())

token = response.json()['access_token']
print(token)
headers_token = {
    'Authorization': f'Bearer {token}'
}
print(headers_token)
get_data = requests.get(url, headers=headers_token)

data = get_date.json()
#print(CLIENT_ID)
#print(CLIENT_SECRET)
#print(SPOTIFY_URL_TOKEN)