from time import sleep
from threading import Thread


# custom thread
class SpotifyPlayerThread(Thread):
    # constructor
    def __init__(self, handsModel, playListID):
        self.handsModel = handsModel
        self.playListID = playListID
        # execute the base constructor
        Thread.__init__(self)

    # function executed in a new thread
    def run(self):
        self.handsModel.activate_playlist_playback(self.playListID)
