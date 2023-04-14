import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import json
import time
import base64

# user-read-private%user-read-email%user-library-read%user-library-modify%user-read-playback-state%user-modify-playback-state%playlist-modify-public%playlist-modify-private%playlist-read-private%playlist-read-collaborative%user-follow-read%user-follow-modify%user-top-read

# AQAm-UyCRTZQKg4GcO-e8iq7fgNHgHFMPB7_FWQ0L_Xdvz8lR0aLA25E7GRC3nbW76_7FWK53vKlv1CX0TgE5WG4KWAwSlk0cwoemXTSFLai0LUcDab5lIecHGUCyDu9DT-WrK23egX2NupmXyanM1G9jqCsoEgYgfpTPMrmMc1fh4WPlp8hIa3iFPHfJ3QIqRGUOHFmc5a5VToWQw

SPOTIPY_CLIENT_ID= "a0b29fd887e24723a4777a236fe5a1c6"
SPOTIPY_CLIENT_SECRET="8231e8527400406cb60505fdf4cc0204"
SPOTIPY_REDIRECT_URI= "http://127.0.0.1:9090"
SCOPE =  "user-read-private user-read-email user-library-read user-library-modify user-read-playback-state user-modify-playback-state playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative user-follow-read user-follow-modify user-top-read"


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE))


def get_access_token(client_id,client_secret):
    # Get an access token using the client credentials flow
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, data={'grant_type': 'client_credentials'})
    print(auth_response.text)
    access_token = auth_response.json()['access_token']
    return access_token


def get_device_id(player):
    devices = player.devices()
    print(devices)
    if devices['devices']:
    # Get the ID of the first available device
        device_id = devices['devices'][0]['id']
    else:
        return "There Are No Active Devices"
    return device_id


def get_playlist_id(access_token,emotion='angry'):
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

def volume_up(player):
    current_volume = player.current_playback()['device']['volume_percent']
    print(f"Current Volume: {current_volume}")
    new_volume = min(100, current_volume + 5)
    player.volume(new_volume)
    print(f"New Volume: {new_volume}")
    return new_volume

def volume_down(player):
    current_volume = player.current_playback()['device']['volume_percent']
    print(f"Current Volume: {current_volume}")
    new_volume = new_volume = max(current_volume - 5, 0)
    player.volume(new_volume)
    print(f"New Volume: {new_volume}")
    return new_volume

def get_current_track_metadata(player):
    current_track = player.current_playback()
    # Extract relevant information
    if current_track is None:
        print("No track is currently playing.")
    else:
        print("----------Current Track Metadata---------- ")
        print(f"Track Name: {current_track['item']['name']} Album Name: {current_track['item']['album']['name']} Artist Name: {current_track['item']['artists'][0]['name']}")

def ac(client_id,client_secret):

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

    
access_token = ac(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET)
print(f'access token: {access_token}')
playlist_id = get_playlist_id(access_token)
time.sleep(3)
device_id = get_device_id(sp)
print("device: ", device_id)
playlist = sp.playlist(playlist_id)
track_uris = [track['track']['uri'] for track in playlist['tracks']['items']]
results = sp.playlist_items(playlist_id, fields="items.track.name,items.track.artists,items.track.uri")
# Print out the track information
for item in results["items"]:
    track = item["track"]
    track_name = track["name"]
    artist_name = track["artists"][0]["name"]
    track_uri = track["uri"]
    print(f"{track_name} by {artist_name} ({track_uri})")
# sp.start_playback(uris=track_uris,device_id=device_id)
# time.sleep(3)

# # Actions
# get_current_track_metadata(sp)
# while True:
#     action = str(input('f - next track p - previous track s - stop track r - resume track u - volume up d volume down'))
#     if action == 'f':
#         sp.next_track()
#         time.sleep(0.5)
#         print('----------Going to next song----------')
#         get_current_track_metadata(sp)
#     elif action == 'p':
#         sp.previous_track()
#         time.sleep(0.5)
#         print('----------Going to previous song----------')
#         get_current_track_metadata(sp)
#     elif action == 's':
#         sp.pause_playback()
#         time.sleep(0.5)
#         print('----------pausing track----------')
#     elif action == 'r':
#         sp.start_playback()
#         time.sleep(0.5)
#         print('----------resuming track----------')
#     elif action == 'u':
#         new_volume = volume_up(sp)
#         time.sleep(0.5)
#     elif action == 'd':
#         new_volume = volume_down(sp)
#         time.sleep(0.5)
#     else:
#         sp.pause_playback()
#         print('done')
#         break


