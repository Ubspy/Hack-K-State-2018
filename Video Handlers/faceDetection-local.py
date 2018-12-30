import cv2
import face_recognition as faceRecognition
import numpy as np
import pickle
import sys

# Additional TODOs in readme file

# Gets data from xml file (not currently working because the encodings are in a seperate dir)
# TODO: Fix getting encodings
data = pickle.loads(open('encodings.xml', "rb").read())

# Previous frame object, this creates a 10 frame buffer for face blurring
# This way if the algorithm loses the face for a few frames the buffer will make up for it
previousFrames = {'one': [], 'two': [], 'three': [], 'four': [], 'five': [], 'six': [], 'seven': [], 'eight': [], 'nine': [], 'ten': []}
faceIdentities = []

# Empty arrays for frames of video
inputFrames = []
outputFrames = []

# Function for bluring a certain area using 2 coordinates
# x1 and y1 are the coordinates for the top left of the rectangle
# x2 and y2 are the coordinates for the bottom right of the rectangle
# Seperate function because the formatting gets weird so this simplifies it a bit
def blurArea(frame, x1, y1, x2, y2):
    # Applies a base blur
    frame[y1:y2, x1:x2] = cv2.blur(frame[y1:y2, x1:x2], (45, 45))

    # Base blur isn't strong enough to hide identity, so it applies a medianBlur several times with a 20 pixel added radius
    for i in range(1, 15):
        frame[y1-20:y2+20, x1-20:x2+20] = cv2.medianBlur(frame[y1-20:y2+20, x1-20:x2+20], 7)

# TODO: Fix this awful ghost blur biz
# This section is a bit ugly, but it was written like this because this was in the last couple hours before demo
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

# This is also a bit ugly, but that's one of the things we intend to fix
# This blurs the 10 frames before the current one
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

# Matches faces to previously added identifiers
def matchFaces(frame, faces):
    for face in faces:
        # Gets encodings from current face in the frame
        # face variable is in array brackets because the method is expecting an array of faces
        # but we did it one at a time, although admittidly a little slow
        encodings = faceRecognition.face_encodings(frame, [face])

        # Checks matching of encodings to known identifiers
        for encoding in encodings:
            matches = faceRecognition.compare_faces(data['encodings'], encoding)
            # Sets default identity to unknown
            name = "Unknown"

        # If there are any matches at all
        if True in matches:
            # Love python syntax, here is returns an array or matched indexes in all the encodings
            # this loops though the matches array and returns indexes which hold True
            matchedIndexes = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # Goes through all matches, and sees which identifier has the most matches
            for currentMatch in matches:
                if currentMatch:
                    # Gets name from matche
                    name = data['names'][matches.index(currentMatch)]
                else:
                    # If no match, set to "Unknown"
                    name = "Unknown"

                # Adds one to the count of the name, uses object so that it works with any set or number of identifier names
                counts[name] = counts.get(name, 0) + 1

            # Gets identifier with maximum matches
            name = max(counts, key=counts.get)

        # global keyword sets scope of local var to the one declared at the top of the script
        global faceIdentities

        # Adds identity to face for the frame
        faceIdentities.append(name)

def processFrame(frame):
    # Converts the frame to grayscale for easier processing
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Finds faces, uses external algorithm to find faces at several angles since cascades weren't doing it
    # TODO: Write own algorithm for more accurate face detection
    faces = faceRecognition.face_locations(grayFrame)

    ghostBlur() # Triggers ghost blur for addition privacy
    swapFrameObjects() # Swaps frame object, don't know why this isn't called in ghostBlur() but at this point I was awake for like 20 hours straight
    matchFaces(frame, faces) # Gets face matchings for the detected faces

    # Gets global face identities
    global faceIdentities

    # For each one that has a set of x and y coords for a bounding rect, it blurs them if the identity is unknown
    for (y1, x2, y2, x1) in faces:
        if faceIdentities[faces.index((y1, x2, y2, x1))] == "Unknown":
            blurArea(frame, x1, y1, x2, y2)
            previousFrames['one'].append((x1, y1, x2, y2))
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) # This is a rectangle to surround the face for debug purposes

    faceIdentities = [] # Resets face identities
    outputFrames.append(frame) # Adds processed frame to output frames

# Original method for bluring faces, was way too long to we replaced it with the above
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

# Gets video from 1st argument when run from the cmd
capture = cv2.VideoCapture(sys.argv[1])

# Reads all frames and puts the into inputFrames array
while(capture.isOpened()):
    ret, frame = capture.read()
    if ret:
        inputFrames.append(frame)
    else:
        break

currentFrame = 1

# Loops through frames and processes them, also outputs progress into console
for frame in inputFrames:
    print("{0}/{1}".format(currentFrame, len(inputFrames)))
    processFrame(frame)
    currentFrame = currentFrame + 1

# Sets up video writer
video = cv2.VideoWriter(sys.argv[2], cv2.VideoWriter_fourcc(*'MP4V'), 20, (640, 480))

# Writes video using outputFrames array
for frame in outputFrames:
    video.write(frame)

# When exited, it closes the stream
cv2.destroyAllWindows()
capture.release()
video.release()
