import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model
from Spotify_final import Spotify


# List Of Gestures:
# play == okay
# stop == stop
# volume up == thumbs up
# volume down == thumbs down
# next track == peace
# previous track == fist
# exit == call me


spotify = Spotify()


def activate_hand_gestures_model(player):
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mpDraw = mp.solutions.drawing_utils

    # Load the gesture recognizer model
    model = load_model('Spotify\Models\Hands\mp_hand_gesture')

    # Load class names
    f = open('Spotify\Models\Hands\gesture.names', 'r')
    classNames = f.read().split('\n')
    f.close()
    print(classNames)

    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    # Set up variables for gesture tracking
    gesture_count = 0
    current_gesture = None

    while True:
        # Read each frame from the webcam
        _, frame = cap.read()

        x, y, c = frame.shape

        # Flip the frame vertically
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get hand landmark prediction
        result = hands.process(framergb)

        className = ''

        # post process the result
        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)

                    landmarks.append([lmx, lmy])

                # Drawing landmarks on frames
                mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

                # Predict gesture
                prediction = model.predict([landmarks])
                classID = np.argmax(prediction)
                className = classNames[classID]
        else:
            className = None

        # Check if the detected gesture is the same as the previous one
        if className == current_gesture and className != None:
            gesture_count += 1
        elif className != current_gesture and className != None:
            current_gesture = className
            gesture_count = 1
        elif className == None:
            gesture_count = 0
        

        # Show the prediction on the frame
        cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2, cv2.LINE_AA)

        # Show the final output
        cv2.imshow("Output", frame)

        # Check if the gesture has been detected for X Frames in a row
        if gesture_count >= 20:
            if className == 'Stop':
                spotify.pause_playback(player)
            elif className == 'Play':
                spotify.start_playback(player)
            elif className == 'Volume Up':
                spotify.volume_up(player)
            elif className == 'Volume Down':
                spotify.volume_down(player)
            elif className == "Next Track":
                spotify.next_track(player)
                spotify.get_current_track_metadata(player)
            elif className == 'Previous Track':
                spotify.previous_track(player)
                spotify.get_current_track_metadata(player)
            elif className == "Exit":
                spotify.pause_playback(player)
                print('Thank You For Using Sound Sensei')
                break


            gesture_count = 0
            current_gesture = None

        if cv2.waitKey(1) == ord('q'):
            break

    # release the webcam and destroy all active windows
    cap.release()
    cv2.destroyAllWindows()

