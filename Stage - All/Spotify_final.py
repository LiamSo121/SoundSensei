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

import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from keras.models import load_model

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


    def get_playlist_id(self,access_token,emotion):
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
    
    def open_spotify(self,username,password):
        # Create Driver And Open Spotify Web 
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach",True)
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
    
    def control_playback(self,player):
        self.get_current_track_metadata(player)

        mpHands = mp.solutions.hands
        hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        mpDraw = mp.solutions.drawing_utils

        # Load the gesture recognizer model
        model = load_model('Spotify\Models\Hands\mp_hand_gesture')

        # Load class names
        f = open('Spotify\Models\Hands\gesture.names', 'r')
        classNames = f.read().split('\n')
        f.close()
        print(classNames)

        # Initialize the webcam
        cap = cv2.VideoCapture(0)

        # Set up variables for gesture tracking
        gesture_count = 0
        current_gesture = None

        while True:
            # Read each frame from the webcam
            _, frame = cap.read()

            x, y, c = frame.shape

            # Flip the frame vertically
            frame = cv2.flip(frame, 1)
            framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get hand landmark prediction
            result = hands.process(framergb)

            className = ''

            # post process the result
            if result.multi_hand_landmarks:
                landmarks = []
                for handslms in result.multi_hand_landmarks:
                    for lm in handslms.landmark:
                        lmx = int(lm.x * x)
                        lmy = int(lm.y * y)

                        landmarks.append([lmx, lmy])

                    # Drawing landmarks on frames
                    mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

                    # Predict gesture
                    prediction = model.predict([landmarks])
                    classID = np.argmax(prediction)
                    className = classNames[classID]
            else:
                className = None

            # Check if the detected gesture is the same as the previous one
            if className == current_gesture and className != None:
                gesture_count += 1
            elif className != current_gesture and className != None:
                current_gesture = className
                gesture_count = 1
            elif className == None:
                gesture_count = 0
            

            # Show the prediction on the frame
            cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2, cv2.LINE_AA)

            # Show the final output
            cv2.imshow("Output", frame)

            # Check if the gesture has been detected for 4 seconds in a row
            if gesture_count >= 20:
                if className == 'stop':
                    player.pause_playback()
                    time.sleep(0.5)
                    print('----------pausing track----------')
                elif className == 'okay':
                    player.start_playback()
                    time.sleep(0.5)
                    print('----------resuming track----------')
                elif className == 'thumbs up':
                    new_volume = self.volume_up(player)
                    time.sleep(0.5)
                elif className == 'thumbs down':
                    try:
                        new_volume = self.volume_down(player)
                    except Exception as e:
                        print(e)
                    time.sleep(0.5)
                elif className == "peace":
                    player.next_track()
                    time.sleep(0.5)
                    print('----------Going to next song----------')
                    self.get_current_track_metadata(player)
                elif className == 'fist':
                    player.previous_track()
                    time.sleep(0.5)
                    print('----------Going to previous song----------')
                    self.get_current_track_metadata(player)
                elif className == "call me":
                    player.pause_playback()
                    print('done')
                    break


                gesture_count = 0
                current_gesture = None

            if cv2.waitKey(1) == ord('q'):
                break

        # release the webcam and destroy all active windows
        cap.release()
        cv2.destroyAllWindows()


