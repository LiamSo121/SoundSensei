import os
import time
from EmotionDetection import EmotionDetection
from Spotify_final import Spotify
from HandIntegration import activate_hand_gestures_model

# List Of Gestures:
# play == okay
# stop == Live Long == stop
# volume up == thumbs up
# volume down == thumbs down
# next track == peace
# previous track == fist
# exit == call me


print("Dear User\nKindly check that your Google Chrome Browser is at least at version 112.0.5615.87\nIf not, Please update your Web Browser before Using SoundSensei")

# Declare Variables
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
face = EmotionDetection()
spotify = Spotify()

# Spotify attributes
client_id = spotify.client_id
client_secret = spotify.client_secret
username = spotify.username
password = spotify.password
player = spotify.sp

# Activate Emotion Detection
emotion = face.activate_camera()
print(f"Chosen Emotion:{emotion}")

# Open Spotify
driver = spotify.open_spotify(username,password)
access_token = spotify.get_access_token(client_id,client_secret)
playlist_id = spotify.get_playlist_id(access_token,emotion)
time.sleep(3)
device_id = spotify.get_device_id(player)
print("device: ", device_id)
playlist = player.playlist(playlist_id)
track_uris = [track['track']['uri'] for track in playlist['tracks']['items']]

# Start Spotify
player.start_playback(uris=track_uris,device_id=device_id)
time.sleep(3)
driver.minimize_window()

# Control Music With Hand Gestures
activate_hand_gestures_model(player)
# Close Chrome
driver.close()








