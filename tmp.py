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

video.release()
