import cv2
import face_recognition as faceRecognition
import numpy as np
import pickle
import sys

data = pickle.loads(open('encodings.xml', "rb").read())

previousFrames = {'one': [], 'two': [], 'three': [], 'four': [], 'five': [], 'six': [], 'seven': [], 'eight': [], 'nine': [], 'ten': []}
faceIdentities = []

#profileCascade = cv2.CascadeClassifier('haarcascade_profileface.xml')

inputFrames = []
outputFrames = []

def blurArea(frame, x1, y1, x2, y2):
    frame[y1:y2, x1:x2] = cv2.blur(frame[y1:y2, x1:x2], (45, 45))

    for i in range(1, 15):
        frame[y1-20:y2+20, x1-20:x2+20] = cv2.medianBlur(frame[y1-20:y2+20, x1-20:x2+20], 7)

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

def ghostBlur():
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

def matchFaces(frame, faces):
    for face in faces:
        encodings = faceRecognition.face_encodings(frame, [face])

        for encoding in encodings:
            matches = faceRecognition.compare_faces(data['encodings'], encoding)
            name = "Unknown"

        if True in matches:
            matchedIndexes = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for currentMatch in matches:
                if currentMatch:
                    name = data['names'][matches.index(currentMatch)]
                else:
                    name = "Unknown"
                counts[name] = counts.get(name, 0) + 1
            name = max(counts, key=counts.get)

        global faceIdentities
        faceIdentities.append(name)

def processFrame(frame):
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceRecognition.face_locations(grayFrame)
    profiles = profileCascade.detectMultiScale(grayFrame, scaleFactor=1.2, minNeighbors=5)

    grayFrame = cv2.flip(grayFrame, 1)
    profilesInv = profileCascade.detectMultiScale(grayFrame, scaleFactor=1.2, minNeighbors=5)

    ghostBlur()
    swapFrameObjects()
    matchFaces(frame, faces)

    global faceIdentities
    for (y1, x2, y2, x1) in faces:
        if faceIdentities[faces.index((y1, x2, y2, x1))] == "Unknown":
            blurArea(frame, x1, y1, x2, y2)
            previousFrames['one'].append((x1, y1, x2, y2))
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    faceIdentities = []
    matchFaces(frame, profiles)

    outputFrames.append(frame)
    faceIdentities = []

'''
    for i, (x, y, width, height) in enumerate(profiles):
        if faceIdentities[i] == "Unknown":
            blurArea(frame, x, y, x + width, y + height)
            x+previousFrames['one'].append((x, y, x + width, y + height))
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 2)

    faceIdentities = []
    matchFaces(frame, profilesInv)

    for i, (x, y, width, height) in enumerate(profilesInv):
        if faceIdentities[i] == "Unknown":
            x = (640 - x)
            blurArea(frame, x, y, x + width, y + height)
            previousFrames['one'].append((x - width, y, x, y + height))
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 2)
'''

capture = cv2.VideoCapture(sys.argv[1])

for frame in capture:
    print("{0}/{1}".format(currentFrame, len(inputFrames)))
    processFrame(frame)
    currentFrame = currentFrame + 1

video = cv2.VideoWriter(sys.arvg[2], cv2.VideoWriter_fourcc(*'MP4V'), 20, (640, 480))

for frame in outputFrames:
    video.write(frame)

# When exited, it closes the stream
cv2.destroyAllWindows()
capture.release()
video.release()
