from deepface import DeepFace
import cv2
import time
import statistics

class EmotionDetection():
    def __init__(self) -> None:
        self.webcam = cv2.VideoCapture(0)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        # org
        self.org = (50, 50)
        # fontScale
        self.fontScale = 1
        # Blue color in BGR
        self.color = (255, 0, 0)
        # Line thickness of 2 px
        self.thickness = 2
        self.start_time = time.time()
        # Create list to append all emotions
        self.emotion_list= []
    def activate_camera(self):
        while True:
            
            (_, image) = self.webcam.read()
            try:
                analysis = DeepFace.analyze(img_path=image, detector_backend="ssd", actions = ["emotion"])
                # font

                emoDict = analysis[0]['emotion']
                max_value = max(emoDict, key=emoDict.get)
                print(max_value)
                if len(self.emotion_list) > 10:
                    self.emotion_list.pop(0)
                self.emotion_list.append(max_value)
                image = cv2.putText(image, max_value, self.org, self.font, self.fontScale, self.color, self.thickness)
                cv2.imshow("test", image)
                cv2.waitKey(3)
            except:
                print("Face could not be detected.")
            if time.time() - self.start_time >= 10:
                break

        print(self.emotion_list)
        self.webcam.release()
        cv2.destroyAllWindows()

        return statistics.mode(self.emotion_list)

