import cv2
import face_recognition as faceRecognition
import numpy as np
import os

# Gets local path
dirPath = os.path.dirname(os.path.realpath(__file__))

# Gets path for faces
facePath = os.path.join(os.path.join(os.getcwd(), 'trainer'), 'faces')
# Gets face files
faceImagePaths = [os.path.join(facePath, f) for f in os.listdir(facePath)]

for faceImage in faceImagePaths:
    image = cv2.imread(faceImage)
    imageGrey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceRecognition.face_locations(imageGrey)

    if len(faces) > 0:
        (x1, y1, x2, y2) = faces[0]
        cv2.imwrite(faceImage, image[y2:y1, x1:x2])

profilePath = os.path.join(os.path.join(os.getcwd(), 'trainer'), 'profiles')
profileImagePaths = [os.path.join(profilePath, f) for f in os.listdir(profilePath)]

profileCascade = cv2.CascadeClassifier('haarcascade_profileface.xml')

for profileImage in profileImagePaths:
    image = cv2.imread(profileImage)
    imageGrey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    profiles = profileCascade.detectMultiScale(imageGrey, scaleFactor=1.2, minNeighbors=10)

    if len(profiles) == 0:
        imageGrey = cv2.flip(imageGrey, 1)
        profiles = profileCascade.detectMultiScale(imageGrey, scaleFactor=1.2, minNeighbors=10)

    if len(profiles) > 0:
        (x, y, width, height) = profiles[0]

    cv2.imwrite(profileImage, image[y:y + height, x:x + width])
