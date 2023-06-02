import Dalle
import Spotify
import EmoModel
import HandsModel
import cv2
import SpotifyQueryThread
import SpotifyPlayerThread
import DalleThread
import yaml
import Radar_Diagram
import statistics


class Handler:

    # --------------------------------------------------#
    # System initialization, Classes, Models and Vars
    # each model and component it a part of the handler CLASS
    # --------------------------------------------------#

    def __init__(self):
        self.states = ['init', 'emo', 'spotifyQuery', 'playlistControl']
        self.nonActiveGesturesList = ['smile', 'live long', 'rock']
        self.state = 'init'
        self.Spotify = Spotify.Spotify()
        self.Dalle = Dalle.Dalle()
        self.EmoModel = EmoModel.EmoModel()
        self.vid = cv2.VideoCapture(0)
        self.isRunning = True
        self.emotion = None
        self.playListID = None
        self.handsModel = None
        self.emotion_list = []
        self.diagram = Radar_Diagram.Diagram()

    def run(self):
        # --------------------------------------------------#
        # Get the frame from the CAMERA Module
        # has to happened each time the func is running
        # --------------------------------------------------#
        diagram_image = None
        ret, frame = self.vid.read()
        frame = cv2.flip(frame, 1)
        originalFrame = frame.copy()
        height, width, _ = frame.shape
        # --------------------------------------------------#
        # System initialization, Handle the connection to the
        # APIs
        # --------------------------------------------------#
        if self.state == 'init':
            with open('config.yaml') as f:
                self.data = yaml.load(f, Loader=yaml.FullLoader)

            self.Spotify.connect(self.Spotify)

            self.state = 'emo'

        # --------------------------------------------------#
        # Get the Prediction form the EMOTION MODEL
        #
        # --------------------------------------------------#
        if self.state == 'emo':
            # add model activation

            emoPredict = self.EmoModel.predict(originalFrame)
            if emoPredict in self.EmoModel.classes:
                self.emotion_list.append(emoPredict)
                diagram_image = self.diagram.create_radar_chart(emoPredict)

                frame = cv2.putText(frame, emoPredict, self.data['camera']['org'], cv2.FONT_HERSHEY_SIMPLEX,
                                    self.data['camera']['fontScale'], self.data['camera']['color'],
                                    self.data['camera']['thickness'])
                # diagram_image = cv2.cvtColor(diagram_image, cv2.COLOR_RGBA2BGR)
                diagram_image = cv2.resize(diagram_image, self.data['diagram']['size'])
                # Calculate the position to place the diagram in the top right corner

                if len(self.emotion_list) == self.data['emotion']['emo_frames']:
                    self.emotion = statistics.mode(self.emotion_list)
                    print(f"Chosen Emotion: {self.emotion}")
                    self.DalleThread = DalleThread.DalleThread(self.Dalle, self.emotion)
                    self.DalleThread.start()
                    self.state = 'spotifyQuery'

        # --------------------------------------------------#
        # Sends the spotify query in a multithread.
        #
        # --------------------------------------------------#
        if self.state == 'spotifyQuery':
            self.SpotifyQueryThread = SpotifyQueryThread.SpotifyQueryThread(self.emotion, self.Spotify)
            self.SpotifyQueryThread.start()
            self.SpotifyQueryThread.join()

            self.playListID = self.SpotifyQueryThread.playListID
            if self.playListID:
                self.handsModel = HandsModel.HandsModel(self.Spotify, self.Dalle, self.emotion,self.data)
                self.state = 'playlistControl'
                frame = originalFrame

        if self.state == 'playlistControl':
            if not self.handsModel.isPlaying:
                self.SpotifyPlayerThread = SpotifyPlayerThread.SpotifyPlayerThread(self.handsModel, self.playListID)
                self.SpotifyPlayerThread.run()

            className, frame = self.handsModel.activate_hand_gestures_model(frame)
            self.handsModel.count_gestures(className)
            if className not in self.nonActiveGesturesList:
                self.handsModel.control_playback(className)
                # Put the text on the frame image
                frame = cv2.putText(frame, className, self.data['camera']['org'], cv2.FONT_HERSHEY_SIMPLEX,
                                    self.data['camera']['fontScale'], self.data['camera']['color'],
                                    self.data['camera']['thickness'])
    


            if self.handsModel.restart:
                self.emotion_list = []
                self.emotion = None
                self.state = 'emo'

        self.frame = frame
        self.diagram_image = diagram_image


if __name__ == '__main__':
    handler = Handler()
    handler.run()
