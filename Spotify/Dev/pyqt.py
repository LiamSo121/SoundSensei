import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
from deepface import DeepFace
import os
import time
import statistics
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout


os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


class VideoCapture(QWidget):
    def __init__(self):
        super().__init__()

        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.org = (50, 50)
        self.fontScale = 1
        self.color = (255, 0, 0)
        self.thickness = 2

        self.video = cv2.VideoCapture(0)

        # Set up the user interface
        self.label = QLabel(self)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # Start the video capture
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # Create list to append all emotions
        self.emotion_list = []

        # Start time for emotion detection
        self.start_time = time.time()

    def update_frame(self):
        _, image = self.video.read()

        try:
            # Convert image to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Perform emotion detection
            analysis = DeepFace.analyze(img_path=image, detector_backend="ssd", actions=["emotion"])
            emoDict = analysis[0]['emotion']
            max_value = max(emoDict, key=emoDict.get)
            self.emotion_list.append(max_value)

            # Draw the emotion label on the image
            image = cv2.putText(image, max_value, self.org, self.font, self.fontScale, self.color, self.thickness)

        except:
            print("Face could not be detected.")

        # Display the video feed in the PyQt window
        image = cv2.resize(image, (640, 480))
        height, width, channel = image.shape
        bytes_per_line = channel * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(q_image))

        # # End video capture after 5 seconds
        # if time.time() - self.start_time >= 5:
        #     self.timer.stop()
        #     self.video.release()
        #     cv2.destroyAllWindows()
        #     print(f"Mode: {statistics.mode(self.emotion_list)}")
        #     QApplication.quit()


if __name__ == '__main__':
    app = QApplication([])
    window = VideoCapture()
    window.show()
    app.exec_()
