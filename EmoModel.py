from deepface import DeepFace


class EmoModel:
    def __init__(self):
        self.prediction = None
        self.classes = ['angry', 'fear', 'disgust', 'happy', 'sad', 'surprise', 'neutral']
        self.emotion_list = []

    def predict(self, frame):

        try:
            analysis = DeepFace.analyze(img_path=frame, detector_backend="ssd", actions=("emotion",), silent=True)
            emoDict = analysis[0]['emotion']
            max_value = max(emoDict, key=emoDict.get)
            if max_value:
                return max_value

        except:
            print("Face could not be detected.")
