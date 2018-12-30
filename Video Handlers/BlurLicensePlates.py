from openalpr import Alpr
import cv2
import threading

import os
import psutil
import time
import sys
process = psutil.Process(os.getpid())



VIDEO_TO_TEST = sys.argv[1]
VIDEO_OUTPUT = sys.argv[2]

BLUR_FACTOR = 40

RESIZE_SIZE = (1280,720)

THREADS = 8 # how many threads to run the program in

GHOST_FRAME_COUNT = 8

segments = []

frames_before = []

# Instantiate an Alpr class
alpr = Alpr("us", "/usr/share/openalpr/config/openalpr.defaults.conf", "/usr/share/openalpr/runtime_data")

# Exit if it is not ready
if not alpr.is_loaded():
    exit(-1)

# Define the opencv capture for the video
cap = cv2.VideoCapture(VIDEO_TO_TEST)

# Make it smoler
cap.set(3,1280)
cap.set(4,720)

# Retrieve the amount of frames in the video (for progress)
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Width and height of the capture
frame_width = cap.get(3)
frame_height = cap.get(4)

# Define the output writer
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(VIDEO_OUTPUT,fourcc, 30, (int(RESIZE_SIZE[0]),int(RESIZE_SIZE[1])))

# Blur frame where it finds a plate
def blurFrame(frame,alprInstance):

	# Resize that boi
	frame = cv2.resize(frame,RESIZE_SIZE)

	# Use ALPR to recognize plates inside the video
	plates = alprInstance.recognize_ndarray(frame)

	for r in frames_before:
		frame[r[0]:r[1],r[2]:r[3]] = cv2.blur(frame[r[0]:r[1],r[2]:r[3]], (BLUR_FACTOR, BLUR_FACTOR))

	# Cycle through the plates and derive a location, only if there is a plate in the frame
	if len(plates["results"]) > 0:

		# Initialize plate_coords
		plate_coords = []

		for plate in plates["results"]:
			plate_coords = plate["coordinates"]

	    # At this point, we have plates in the frame along with their locations, now we make the rectangle
		x = plate_coords[0]['x']
		y = plate_coords[0]['y']

		w = plate_coords[2]['x'] - x
		h = plate_coords[2]['y'] - y

	    # Now we blur the part of the frame with the license plate in it
		frame[y:y + h, x:x + w] = cv2.blur(frame[y:y + h, x:x + w], (BLUR_FACTOR, BLUR_FACTOR))

		frames_before.insert(0,[y,y+h,x,x+w])
		try:
			frames_before.pop(GHOST_FRAME_COUNT)
		except IndexError:
			pass

	    # Now give the frame back
		return frame
	else:
		# Just return the original frame, since there are no plates
		return frame

# Shorthand for displaying opencv frame
def showFrame(frame):

	# Show the image in an opencv frame
	cv2.imshow("frame",frame)

	# Make sure to break out of loop when q key is pressed
	if cv2.waitKey(1) & 0xFF == ord('q'):
		return False

    # If not pressing key, return true
	return True

# Splits the capture into Frames/Threads amount of portions
def splitCapture(capture, frames=[]):
	# Amount of frames per section
	frames_per_section = length/THREADS

	# Frames
	theseFrames = frames

	# Sections array, return value
	sections = []

	# Create sections looping through frames
	if frames == []:
		frameCount = 0
		while capture.isOpened():
			ret, frame = capture.read()
			theseFrames.append(frame)
			frameCount += 1

			#print("{}/{}".format(frameCount,length))

			if frameCount == length:
				break

	for i in range(THREADS):
		k = int(i*frames_per_section+frames_per_section)
		sections.append(frames[int(i*frames_per_section):k])

	capture.release()

	return sections

# Method to take capture segments and detect them through ALPR
def detectSegment(segment,alprInstance,idA):
	# # Uhh ok dont look at this
	# segment.pop(0)

	# Loop through all frames in segment
	for i in range(len(segment)):
		# Blur each frame
		if segment[i] is None:
			continue
		#print("Thread : {} -- {}/{}\n".format(idA, i,len(segment)))
		segment[i] = blurFrame(segment[i],alprInstance)
	# Return the segment
	segments.insert(idA, segment)
	return True

class DetectThread (threading.Thread):
	def __init__(self, threadID, segment, alprInstance):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.segment = segment
		self.alprInstance = alprInstance
	def run(self):
		#print(len(self.segment))
		detectSegment(self.segment,self.alprInstance,self.threadID)

# Main method to call all testing code etc
def main():

	# times = time.time()
	# frames = []
	# while(time.time()-times < 10):
	# 	ret,frame = cap.read()
	# 	frames.append(frame)

	# Split the frames into equal portions
	segments = splitCapture(cap)

	threads = []

	for i in range(THREADS):
		alpr = Alpr("us", "/usr/share/openalpr/config/openalpr.defaults.conf", "/usr/share/openalpr/runtime_data")
		t = DetectThread(i,segments[i],alpr)
		threads.append(t)
		t.start()

	for i in range(THREADS):
		threads[i].join()

	for i in range(len(segments)):
		for k in range(len(segments[i])):
			out.write(segments[i][k])

	cap.release()
	out.release()
	# while(cap.isOpened()):
	# 	ret, frame = cap.read()
	# 	showFrame(blurFrame(frame,alpr))


# Call the main function
main()
