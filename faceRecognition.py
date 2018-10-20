import cv2
import face_recognition as faceRecognition
import numpy as np
import time

# Sets camera object
camera = cv2.VideoCapture(0)

camera.set(3, 640)
camera.set(4, 480)

def processFrame(frame):
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceRecognition.face_locations(grayFrame)
    profiles = profileCascade.detectMultiScale(grayFrame, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))

    grayFrame = cv2.flip(grayFrame, 1)
    profilesInv = profileCascade.detectMultiScale(grayFrame, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))

    for (y1, x1, y2, x2) in faces:
        #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        frame[y1:y2, x2:x1] = cv2.blur(frame[y1:y2, x2:x1], (50, 50))

    for (x, y, width, height) in profiles:
        #cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 2)
        frame[y:(y + height), x:(x + width)] = cv2.blur(frame[y:(y + height), x:(x + width)], (50, 50))

    for (x, y, width, height) in profilesInv:
        x = (640 - x)
        #cv2.rectangle(frame, (x, y), (x - width, y + height), (0, 255, 0), 2)
        frame[y:(y + height), (x - width):x] = cv2.blur(frame[y:(y + height), (x - width):x], (50, 50))

    outputFrames.append(frame)

profileCascade = cv2.CascadeClassifier('haarcascade_profileface.xml')

inputFrames = []
outputFrames = []

timeout = time.time() + 10

while(True):
    # Captures video for frame
    ret, frame = camera.read()

    inputFrames.append(frame)

    if time.time() > timeout:
        break

camera.release()
currentFrame = 0

for frame in inputFrames:
    print("{0}/{1}".format(currentFrame, len(inputFrames)))
    processFrame(frame)
    currentFrame = currentFrame + 1

video = cv2.VideoWriter('gay.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 20, (640, 480))

for frame in outputFrames:
    video.write(frame)

# When exited, it closes the stream
cv2.destroyAllWindows()
video.release()
