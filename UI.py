import cv2
from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QImage, QPixmap

from UIwindow import UIwindow
from PyQt5.QtCore import QTimer
from Handler import Handler
from pathlib import Path
import PyQt5
import threading
import pandas as pd
import time
import os

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.fspath(
    Path(PyQt5.__file__).resolve().parent / "Qt5" / "plugins"
)


# Main window class, this window runs the other windows in main file, this saves the UI files and dosent change them
# the only change that has occurred it's the inheritance of the Ui_Form from QtWidgets.QtWidget
# this way gives us the option to run, show and hide the windows whenever we want and manipulate them
# for our desire.


# creating the main class, the QWidget is the base class for all user interface.
class MainWindow(qtw.QWidget):
    # init is the constructor of the class, it is called when an object is created.
    # here we initialize the class with the super class(QWidget)
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.handler = Handler()

        self.ui = UIwindow()  # creating the ui class of the first window
        self.ui.setupUi(self.ui)
        self.ui.show()
        self.ui.header.setText("Welcome TO SoundSensei! ")
        # timer
        self.timer = QTimer(self)
        
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(33)  # Update every 1 second

    def update_labels(self):
        # Call the run function of the Handler class to get the frames
        try:
            self.handler.run()
        except:
            print("Internet connection Issue")
            quit()
        # Convert frames to QImage and display them in QLabel
        try:
            self.ui.theFrame.setPixmap(self.convert_nparray_to_QPixmap(self.handler.frame))
            if self.handler.state == 'emo':
                self.ui.diagram.setPixmap(self.convert_nparray_to_QPixmap(self.handler.diagram_image))
            else:
                self.ui.songInfo.setText(self.handler.Spotify.current_track_info)
                self.ui.diagram.setPixmap(self.convert_nparray_to_QPixmap(self.handler.DalleThread.image))

        except:
            pass

    def convert_nparray_to_QPixmap(self, img):
        w, h, ch = img.shape
        # Convert resulting image to pixmap
        if img.ndim == 1:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        qimg = QImage(img.data, h, w, 3 * h, QImage.Format_RGB888)
        qpixmap = QPixmap(qimg)

        return qpixmap


# The idea is to import all the UI files, attributes classes and the recording tool functionalities
# and then run the main window class and the functionalities of the recording tool
# save the data that gathered from the user inside the attributes classes
# to DataFrame, and then save the dataframe to a csv file.


if __name__ == "__main__":
    app = qtw.QApplication([])
    window = MainWindow()
    app.exec_()
