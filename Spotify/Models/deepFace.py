from deepface import DeepFace
import os
import cv2
import time
import statistics


os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


webcam = cv2.VideoCapture(0)

font = cv2.FONT_HERSHEY_SIMPLEX


# org
org = (50, 50)

# fontScale
fontScale = 1

# Blue color in BGR
color = (255, 0, 0)

# Line thickness of 2 px
thickness = 2
start_time = time.time()

# Create list to append all emotions
emotion_list= []

while True:
    
    (_, image) = webcam.read()
    try:
        analysis = DeepFace.analyze(img_path=image, detector_backend="ssd", actions = ["emotion"])
        # font

        emoDict = analysis[0]['emotion']
        max_value = max(emoDict, key=emoDict.get)
        print(max_value)
        emotion_list.append(max_value)
        image = cv2.putText(image, max_value, org, font, fontScale, color, thickness)
        cv2.imshow("test", image)
        cv2.waitKey(3)
    except:
        print("Face could not be detected.")
    if time.time() - start_time >= 5:
        break

print(emotion_list)
webcam.release()
cv2.destroyAllWindows()

print(f"Mode: {statistics.mode(emotion_list)}")
