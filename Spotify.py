import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import json
import time
import base64
import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service







class Spotify:
    load_dotenv()
    def __init__(self):
        self.client_id = os.getenv("CLIENT_ID")
        # self.client_id = "33b9471f705546e1a0b6deae9edfc6dc"
        self.client_secret = os.getenv("CLIENT_SECRET")
        # self.client_secret = "a06ff14da97540bd8bd9e72a385a7300"
        self.redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
        # self.redirect_uri = "http://127.0.0.1:9090"
        self.scope = os.getenv("SCOPE")
        # self.scope = "user-read-private user-read-email user-library-read user-library-modify user-read-playback-state user-modify-playback-state playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative user-follow-read user-follow-modify user-top-read"
        self.username = os.getenv("EMAIL")
        # self.username = "itziktheliquid@gmail.com"
        self.password = os.getenv("PASSWORD")
        # self.password = "LiamSobol123"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri, scope=self.scope))
        self.access_token = None
        self.device_id = None
        self.track_uri_list = None

    def connect(self,spotify):
        driver = self.open_spotify(self.username, self.password)
        spotify.access_token = self.get_access_token(self.client_id, self.client_secret)
        time.sleep(3)
        spotify.device_id = self.get_device_id(self.sp)
        print("device: ", spotify.device_id)
        time.sleep(3)
        self.activate_spotify_playback()
        driver.minimize_window()



    def open_spotify(self,username,password):
        # Create Driver And Open Spotify Web 
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        path = './chromedriver'
        service = Service(path)
        driver = webdriver.Chrome(service=service,options=options)
        driver.get("https://www.spotify.com/login/")
        # Find the username and password input fields, and fill them in with your credentials
        username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-username")))
        username_field.send_keys(username)
        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-password")))
        password_field.send_keys(password)
        # Submit the login form
        password_field.send_keys(Keys.RETURN)
        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.title_contains("Spotify"))
        openS = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "svelte-1gcdbl9")))
        openS.click()
        return driver
    

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
    
    def get_current_track_metadata(self,player,tracks_uri_list):
        time.sleep(0.3)
        current_track = player.current_playback()  # Retrieve currently playing track
        temp_track_id = current_track['item']['id']  # Extract the ID of the current track
        current_track_id = f"spotify:track:{temp_track_id}"


        next_track_index = tracks_uri_list.index(current_track_id) + 1  # Calculate the index of the next track
        next_track_uri = tracks_uri_list[next_track_index]
        next_track_name = self.get_tracks_name(next_track_uri)

        previous_track_index = tracks_uri_list.index(current_track_id) - 1
        previous_track_uri = tracks_uri_list[previous_track_index]
        previous_track_name = self.get_tracks_name(previous_track_uri)

        if current_track is None:
            print("No track is currently playing.")
        else:
            try:
                self.current_track_info = f"Track Name: {current_track['item']['name']} • Album Name: {current_track['item']['album']['name']} • Artist Name: {current_track['item']['artists'][0]['name']} • Next Track Name: {next_track_name} • Previous Track Name: {previous_track_name}"
                self.current_track = current_track['item']['name']
            except Exception as e:
                print(e)

    def get_playlist_id(self,emotion,access_token):
        endpoint = 'https://api.spotify.com/v1/search'
        # Set the query parameters for the API request
        query_params = {
            'type': 'playlist',
            'q': f'emotion:{emotion}',
            'limit': 3

        }
        # Set up the API request headers with the access token
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        # Make the API request
        response = requests.get(endpoint, params=query_params, headers=headers)
        # Parse the JSON response
        response_json = json.loads(response.text)
        playlist_uris = []
        if 'playlists' in response_json:
            playlists = response_json['playlists']
            if 'items' in playlists:
                for item in playlists['items']:
                    if 'uri' in item:
                        playlist_uris.append(item['uri'])

        playlist_id = random.choice(playlist_uris)

        print(playlist_id)
        

        # playlist_id = "spotify:playlist:7GhawGpb43Ctkq3PRP1fOL"
        return playlist_id



    def get_tracks_name(self,track_uri):
        # Make a GET request to the Spotify API to get the track information
        track_url = f'https://api.spotify.com/v1/tracks/{track_uri.split(":")[2]}'  # Extract the track ID from the URI

        headers = {'Authorization': f'Bearer {self.access_token}'}

        response = requests.get(track_url, headers=headers)

        # Extract the track name from the response
        track_name = response.json()['name']

        return track_name



    def get_device_id(self,player):
        devices = player.devices()
        if devices['devices']:
        # Get the ID of the first available device
            device_id = devices['devices'][0]['id']
        else:
            return "There Are No Active Devices"
        return device_id

    def activate_spotify_playback(self):
        # add volume 0 while activate
        track_uri = "spotify:track:1BMFet4vUoOgpLYIl3kVMQ"
        # Start playing the track
        print(self.device_id)
        self.sp.start_playback(uris=[track_uri],device_id=self.device_id)
        time.sleep(1)
        self.sp.pause_playback()

    def pause_playback(self,player):
        player.pause_playback()
        time.sleep(0.1)
        print('----------pausing track----------')

    def start_playback(self,player):
        player.start_playback()
        time.sleep(0.1)
        print('----------resuming track----------')
    def next_track(self,player):
        player.next_track()
        time.sleep(0.1)
        print('----------Going to next song----------')
    def previous_track(self,player):
        player.previous_track()
        time.sleep(0.1)
        print('----------Going to previous song----------')
    
    def volume_down(self,player):
        try:
            current_volume = player.current_playback()['device']['volume_percent']
            print(f"Current Volume: {current_volume}")
            new_volume = new_volume = max(current_volume - 15, 0)
            player.volume(new_volume)
            print(f"New Volume: {new_volume}")
        except Exception as e:
            print(e)
        time.sleep(0.3)

    def volume_up(self,player):
        try:
            current_volume = player.current_playback()['device']['volume_percent']
            print(f"Current Volume: {current_volume}")
            new_volume = min(100, current_volume + 15)
            player.volume(new_volume)
            print(f"New Volume: {new_volume}")
        except Exception as e:
            print(e)
        time.sleep(0.3)
        
