import cv2
import face_recognition as faceRecognition
import numpy as np
import time

previousFrames = {'one': [], 'two': [], 'three': [], 'four': [], 'five': [], 'six': [], 'seven': [], 'eight': [], 'nine': [], 'ten': []}

def blurArea(frame, x1, y1, x2, y2):
    frame[y1:y2, x2:x1] = cv2.blur(frame[y1:y2, x2:x1], (45, 45))

    for i in range(1, 15):
        frame[y1-20:y2+20, x2-20:x1+20] = cv2.medianBlur(frame[y1-20:y2+20, x2-20:x1+20], 7)

def swapFrameObjects():
    previousFrames['ten'] = previousFrames['nine']
    previousFrames['nine'] = previousFrames['eight']
    previousFrames['eight'] = previousFrames['seven']
    previousFrames['seven'] = previousFrames['six']
    previousFrames['six'] = previousFrames['five']
    previousFrames['five'] = previousFrames['four']
    previousFrames['four'] = previousFrames['three']
    previousFrames['three'] = previousFrames['two']
    previousFrames['two'] = previousFrames['one']
    previousFrames['one'] = []

def processFrame(frame):
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceRecognition.face_locations(grayFrame)
    profiles = profileCascade.detectMultiScale(grayFrame, scaleFactor=1.2, minNeighbors=5)

    grayFrame = cv2.flip(grayFrame, 1)
    profilesInv = profileCascade.detectMultiScale(grayFrame, scaleFactor=1.2, minNeighbors=5)

    for (x1, y1, x2, y2) in previousFrames['one']:
        blurArea(frame, x1, y1, x2, y2)

    for (x1, y1, x2, y2) in previousFrames['two']:
        blurArea(frame, x1, y1, x2, y2)

    for (x1, y1, x2, y2) in previousFrames['three']:
        blurArea(frame, x1, y1, x2, y2)

    for (x1, y1, x2, y2) in previousFrames['four']:
        blurArea(frame, x1, y1, x2, y2)

    for (x1, y1, x2, y2) in previousFrames['five']:
        blurArea(frame, x1, y1, x2, y2)

    for (x1, y1, x2, y2) in previousFrames['six']:
        blurArea(frame, x1, y1, x2, y2)

    for (x1, y1, x2, y2) in previousFrames['seven']:
        blurArea(frame, x1, y1, x2, y2)

    for (x1, y1, x2, y2) in previousFrames['eight']:
        blurArea(frame, x1, y1, x2, y2)

    for (x1, y1, x2, y2) in previousFrames['nine']:
        blurArea(frame, x1, y1, x2, y2)

    for (x1, y1, x2, y2) in previousFrames['ten']:
        blurArea(frame, x1, y1, x2, y2)

    swapFrameObjects()

    for (y1, x1, y2, x2) in faces:
        blurArea(frame, x1, y1, x2, y2)
        previousFrames['one'].append((x1, y1, x2, y2))

    for (x, y, width, height) in profiles:
        blurArea(frame, x + width, y, x, y + height)
        previousFrames['one'].append((x + width, y, x, y + height))

    for (x, y, width, height) in profilesInv:
        x = (640 - x)
        blurArea(frame, x, y, x - width, y + height)
        previousFrames['one'].append((x, y, x - width, y + height))

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
