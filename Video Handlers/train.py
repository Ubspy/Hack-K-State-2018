import cv2
import face_recognition as faceRecognition
import numpy as np
import os
import pickle

# Unreferenced everywhere else, not enough time to integrate into site, adds face identities

# Gets local path
dirPath = os.path.dirname(os.path.realpath(__file__))

# TODO: Get these files from the right spot
# Gets path for faces
facePath = os.path.join(os.path.join(os.getcwd(), 'trainer'), 'faces')
# Gets face files
# TODO: Get these files from the right spot
faceImagePaths = [os.path.join(facePath, f) for f in os.listdir(facePath)]

profilePath = os.path.join(os.path.join(os.getcwd(), 'trainer'), 'profiles')
profileImagePaths = [os.path.join(profilePath, f) for f in os.listdir(profilePath)]

# Uses haar cascade to get faces
profileCascade = cv2.CascadeClassifier('haarcascade_profileface.xml')

knownNames = []
knownEncodings = []

num = 1

# Loops through faces and profiles and adds encodings
# reason it's seperated into face and profiles and flipped profiles is because originally the program was to use haar cascades not a custom alg
# TODO: clean up using custom face detection algorithm
for faceImage in faceImagePaths:
    print("{}/{}".format(num, len(faceImagePaths) + len(profileImagePaths)))
    num += 1

    name = "Jack Moren"
    image = cv2.imread(faceImage)
    rgbImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    faces = faceRecognition.face_locations(rgbImage)
    encodings = faceRecognition.face_encodings(rgbImage, faces)

    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(name)

for profileImage in profileImagePaths:
    print("{}/{}".format(num, len(faceImagePaths) + len(profileImagePaths)))
    num += 1

    name = "Jack Moren"
    image = cv2.imread(faceImage)
    rgbImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    profiles = profileCascade.detectMultiScale(rgbImage, scaleFactor=1.2, minNeighbors=5)
    encodings = faceRecognition.face_encodings(rgbImage, profiles)

    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(name)

    rgbImage = cv2.flip(rgbImage, 1)
    profilesInv = profileCascade.detectMultiScale(rgbImage, scaleFactor=1.2, minNeighbors=5)
    encodings = faceRecognition.face_encodings(rgbImage, profilesInv)

    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(name)

faceData = {'encodings': knownEncodings, 'names': knownNames}

# TODO: Get this file from the right spot
f = open("encodings.xml", "wb")
f.write(pickle.dumps(faceData))
f.close()
