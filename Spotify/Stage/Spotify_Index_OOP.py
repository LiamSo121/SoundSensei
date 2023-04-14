import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import json
import time
import base64
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# user-read-private%user-read-email%user-library-read%user-library-modify%user-read-playback-state%user-modify-playback-state%playlist-modify-public%playlist-modify-private%playlist-read-private%playlist-read-collaborative%user-follow-read%user-follow-modify%user-top-read

# AQAm-UyCRTZQKg4GcO-e8iq7fgNHgHFMPB7_FWQ0L_Xdvz8lR0aLA25E7GRC3nbW76_7FWK53vKlv1CX0TgE5WG4KWAwSlk0cwoemXTSFLai0LUcDab5lIecHGUCyDu9DT-WrK23egX2NupmXyanM1G9jqCsoEgYgfpTPMrmMc1fh4WPlp8hIa3iFPHfJ3QIqRGUOHFmc5a5VToWQw

class Spotify():
    load_dotenv()
    def __init__(self) -> None: 
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
        self.scope = os.getenv("SCOPE")
        self.username = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri, scope=self.scope))


    def get_device_id(self,player):
        devices = player.devices()
        print(devices)
        if devices['devices']:
        # Get the ID of the first available device
            device_id = devices['devices'][0]['id']
        else:
            return "There Are No Active Devices"
        return device_id


    def get_playlist_id(self,access_token,emotion='dark'):
        endpoint = 'https://api.spotify.com/v1/search'
        # Set the query parameters for the API request
        query_params = {
            'type': 'playlist',
            'q': emotion,
        }
        # Set up the API request headers with the access token
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        # Make the API request
        response = requests.get(endpoint, params=query_params, headers=headers)
        # Parse the JSON response
        response_json = json.loads(response.text)
        # Extract the playlist URI from the response
        playlist_id = response_json['playlists']['items'][0]['uri']
        return playlist_id

    def volume_up(self,player):
        current_volume = player.current_playback()['device']['volume_percent']
        print(f"Current Volume: {current_volume}")
        new_volume = min(100, current_volume + 5)
        player.volume(new_volume)
        print(f"New Volume: {new_volume}")
        return new_volume

    def volume_down(self,player):
        current_volume = player.current_playback()['device']['volume_percent']
        print(f"Current Volume: {current_volume}")
        new_volume = new_volume = max(current_volume - 5, 0)
        player.volume(new_volume)
        print(f"New Volume: {new_volume}")
        return new_volume

    def get_current_track_metadata(self,player):
        current_track = player.current_playback()
        # Extract relevant information
        if current_track is None:
            print("No track is currently playing.")
        else:
            print("----------Current Track Metadata---------- ")
            print(f"Track Name: {current_track['item']['name']} Album Name: {current_track['item']['album']['name']} Artist Name: {current_track['item']['artists'][0]['name']}")

    def get_access_token(self,client_id,client_secret):

        # Encode the client ID and client secret as base64
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

        # Set up the request headers and parameters
        headers = {
            'Authorization': f"Basic {client_creds_b64}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {'grant_type': 'client_credentials'}

        # Send the POST request to get the access token
        response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)

        # Parse the response JSON to get the access token
        access_token = response.json()['access_token']

        return access_token





def main():
    spotify = Spotify()
    client_id = spotify.client_id
    client_secret = spotify.client_secret
    username = spotify.username
    password = spotify.password
    player = spotify.sp


    
    access_token = spotify.get_access_token(client_id,client_secret)
    print(f'access token: {access_token}')
    playlist_id = spotify.get_playlist_id(access_token)
    time.sleep(3)
    device_id = spotify.get_device_id(player)
    print("device: ", device_id)
    playlist = player.playlist(playlist_id)
    track_uris = [track['track']['uri'] for track in playlist['tracks']['items']]
    player.start_playback(uris=track_uris,device_id=device_id)
    time.sleep(3)

    # Actions
    spotify.get_current_track_metadata(player)
    while True:
        action = str(input('f - next track p - previous track s - stop track r - resume track u - volume up d volume down'))
        if action == 'f':
            player.next_track()
            time.sleep(0.5)
            print('----------Going to next song----------')
            spotify.get_current_track_metadata(player)
        elif action == 'p':
            player.previous_track()
            time.sleep(0.5)
            print('----------Going to previous song----------')
            spotify.get_current_track_metadata(player)
        elif action == 's':
            player.pause_playback()
            time.sleep(0.5)
            print('----------pausing track----------')
        elif action == 'r':
            player.start_playback()
            time.sleep(0.5)
            print('----------resuming track----------')
        elif action == 'u':
            new_volume = spotify.volume_up(player)
            time.sleep(0.5)
        elif action == 'd':
            new_volume = spotify.volume_down(player)
            time.sleep(0.5)
        else:
            player.pause_playback()
            print('done')
            break




main()