from time import sleep
from threading import Thread


# custom thread
class DalleThread(Thread):
    # constructor
    def __init__(self,dalle,emotion):
        # execute the base constructor
        Thread.__init__(self)
        self.dalle = dalle
        self.emotion = emotion
        self.image = None    # function executed in a new thread
    def run(self):
        self.image = self.dalle.generate_image(self.emotion)
        
