import os
import time
from deepface_OOP import EmotionDetection
from Spotify_final import Spotify
import threading


os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
face = EmotionDetection()
spotify = Spotify()


client_id = spotify.client_id
client_secret = spotify.client_secret
username = spotify.username
password = spotify.password
player = spotify.sp

emotion = face.activate_camera()
print(emotion)


driver = spotify.open_spotify(username,password)


access_token = spotify.get_access_token(client_id,client_secret)
playlist_id = spotify.get_playlist_id(access_token,emotion)

time.sleep(3)
device_id = spotify.get_device_id(player)
print("device: ", device_id)

playlist = player.playlist(playlist_id)
track_uris = [track['track']['uri'] for track in playlist['tracks']['items']]
player.start_playback(uris=track_uris,device_id=device_id)

time.sleep(3)
driver.minimize_window()
spotify.control_playback(player)








