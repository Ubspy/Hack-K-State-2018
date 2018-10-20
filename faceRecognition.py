import cv2
import face_recognition as faceRecognition
import numpy as np

# Sets camera object
camera = cv2.VideoCapture(0)

camera.set(3, 640);
camera.set(4, 480);

profileCascade = cv2.CascadeClassifier('haarcascade_profileface.xml')

while(True):
    # Captures video for frame
    ret, frame = camera.read()

    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceRecognition.face_locations(grayFrame)

    profiles = profileCascade.detectMultiScale(grayFrame, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))

    grayFrame = cv2.flip(grayFrame, 1)

    profilesInv = profileCascade.detectMultiScale(grayFrame, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))

    for (y1, x1, y2, x2) in faces:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    for (x, y, width, height) in profiles:
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 2)

    for (x, y, width, height) in profilesInv:
        x = (640 - x)
        cv2.rectangle(frame, (x, y), (x - width, y + height), (0, 255, 0), 2)

    # Display frame
    cv2.imshow('camera', frame)

    # Close key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When exited, it closes the stream
camera.release()
cv2.destroyAllWindows()
