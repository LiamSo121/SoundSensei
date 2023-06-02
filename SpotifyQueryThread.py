from time import sleep
from threading import Thread


# custom thread
class SpotifyQueryThread(Thread):
    # constructor
    def __init__(self, emotion, Spotify):
        self.emotion = emotion
        self.Spotify = Spotify
        # execute the base constructor
        Thread.__init__(self)
        # set a default value
        self.playListID = None

    # function executed in a new thread
    def run(self):
        self.playListID = self.Spotify.get_playlist_id(self.emotion,self.Spotify.access_token)
