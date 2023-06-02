import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model
import time
import random
import DalleThread


# List Of Gestures:
# play == okay
# stop == stop
# volume up == thumbs up
# volume down == thumbs down
# next track == peace
# previous track == fist
# exit == call me




class HandsModel:
    def __init__(self,spotify,dalle,emotion,data):
        self.spotify = spotify
        self.restart = False
        self.dalle = dalle
        self.model = load_model('mp_hand_gesture')
        self.classNames = open('gesture.names', 'r').read().split('\n')
        self.emotion = emotion
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands=1, min_detection_confidence=0.85)
        self.mpDraw = mp.solutions.drawing_utils
        self.current_gesture = None
        self.gesture_count = 0
        self.isPlaying = False
        self.image = None
        self.dalle_thread = DalleThread.DalleThread(self.dalle,self.emotion)
        self.nonActiveGesturesList = ['smile','live long','rock']
        self.data = data



    def activate_playlist_playback(self,playlist_id):
        playlist = self.spotify.sp.playlist(playlist_id)
        track_uris = [track['track']['uri'] for track in playlist['tracks']['items']]
        
        random.shuffle(track_uris)

        self.spotify.track_uri_list = track_uris
        try:
            self.spotify.sp.start_playback(uris=track_uris,device_id= self.spotify.device_id)
            self.spotify.get_current_track_metadata(self.spotify.sp,self.spotify.track_uri_list)
            # self.dalle.generate_image(self.emotion,self.spotify.current_track)
            self.isPlaying = True
        except Exception as e:
            print(e)


    def activate_hand_gestures_model(self,frame):
        x, y, c = frame.shape

        # Get hand landmark prediction
        result = self.hands.process(frame)

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
                self.mpDraw.draw_landmarks(frame, handslms, self.mpHands.HAND_CONNECTIONS)
                # Predict gesture
                prediction = self.model.predict([landmarks])
                classID = np.argmax(prediction)
                className = self.classNames[classID]
  

        return className,frame



    def count_gestures(self,className):
        # Check if the detected gesture is the same as the previous one
        if className == self.current_gesture and className != '':
            self.gesture_count += 1
        elif className != self.current_gesture and className != '':
            self.current_gesture = className
            self.gesture_count = 1
        elif className == '':
            self.gesture_count = 0
        elif className == 'smile' or className == 'live long' or className == 'rock':
            self.gesture_count = 0

    def control_playback(self,className):
        # Check if the gesture has been detected for X Frames in a row
        if self.gesture_count == self.data['hands']['size']:
            if className == 'Stop':
                self.spotify.pause_playback(self.spotify.sp)
            elif className == 'Play':
                self.spotify.start_playback(self.spotify.sp)
            elif className == 'Volume Up':
                self.spotify.volume_up(self.spotify.sp)
            elif className == 'Volume Down':
                self.spotify.volume_down(self.spotify.sp)
            elif className == "Next Track":
                self.spotify.next_track(self.spotify.sp)
                self.spotify.get_current_track_metadata(self.spotify.sp,self.spotify.track_uri_list)
            elif className == 'Previous Track':
                self.spotify.previous_track(self.spotify.sp)
                self.spotify.get_current_track_metadata(self.spotify.sp,self.spotify.track_uri_list)
            elif className == "Restart":
                self.spotify.pause_playback(self.spotify.sp)
                self.restart = True
            self.gesture_count = 0

