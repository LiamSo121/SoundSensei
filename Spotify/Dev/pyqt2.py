from deepface import DeepFace
import os
import cv2
import time
import statistics
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel


class VideoCapture:
    def __init__(self, video_source=0):
        self.capture = cv2.VideoCapture(video_source)
        self.timer = QTimer()
        self.timer.timeout.connect(self.get_frame)
        self.frame = None

    def start(self):
        self.timer.start(30)

    def stop(self):
        self.timer.stop()
        self.capture.release()

    def get_frame(self):
        ret, frame = self.capture.read()
        if ret:
            self.frame = frame.copy()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.video = VideoCapture()
        self.label = QLabel(self)
        self.setCentralWidget(self.label)
        self.video.start()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        self.start_time = time.time()
        self.emotion_list = []

    def update_frame(self):
        if self.video.frame is not None:
            frame = cv2.cvtColor(self.video.frame, cv2.COLOR_BGR2RGB)
            try:
                analysis = DeepFace.analyze(img_path=frame, detector_backend="ssd", actions=["emotion"])
                emoDict = analysis[0]['emotion']
                max_value = max(emoDict, key=emoDict.get)
                print(max_value)
                self.emotion_list.append(max_value)
                frame = cv2.putText(frame, max_value, org, font, fontScale, color, thickness)
            except:
                print("Face could not be detected.")
            self.show_frame(frame)

        if time.time() - self.start_time >= 15:
            self.video.stop()
            self.timer.stop()
            print(f"Mode: {statistics.mode(self.emotion_list)}")
            cv2.destroyAllWindows()

    def show_frame(self, frame):
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.label.setPixmap(pixmap)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
