import cv2
import face_recognition as faceRecognition
import numpy as np
import time

initialTime = time.time()

camera = cv2.VideoCapture(0)

camera.set(3, 640) # set video widht
camera.set(4, 480) # set video height

imagesOfFace = []

currentCap = 0

# Runs video capture for 20 seconds
while (time.time() - initialTime) < 20:
    # Captures video for frame
    ret, frame = camera.read()

    greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceRecognition.face_locations(greyFrame)

    # Gets a bunch of face images for processing
    if faces and currentCap % 10 == 0:
        (y1, x2, y2, x1) = faces[0]
        cv2.imwrite(('trainer/faces/face-' + str(time.time()) + '.jpg'), greyFrame[y1:y2, x1:x2])

    currentCap += 1

    # Shows image in frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(10) == 27:
        break

camera.release()
cv2.destroyAllWindows()
