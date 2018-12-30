# Aut0Blur
This project was created for the 2018 K-State Hackathon. This is the NOT original code, to see the archived code [click here](https://github.com/Ubspy/Hack-K-State-2018/tree/archive/hackathon-archive).

# What does it do?
Given a video file, it will blur out unrecognized faces and license plates.

# What are all these files?
**Encodings:** These files are encodings for identifiers attached to a particular person's face
**Video Handlers:** These files are the python scripts that process the image
+ **BlurLicensePlates.py:** This is the script to recognize and blur and license plates found in the video
+ **faceDetection.py:** These are the scripts for detecting, identifying, and bluring faces found in the video. Look at the local file for documentation
+ **gatherFaceData.py:** This file is to gather several images of a person's face so we can gather encodings to make face identifiers
+ **train.py:** This file generates encodings for a particular face identifier, currently hard-coded to make identifiers for one particular person

**Web:** These are the website files for the website used to demo the program

# Why is this important?
Many people complain about being posted on the web without consent. For example, Youtube has to deal with privacy complaints on a daily basis, forcing content creators to take the video down and if they still have it, they can re-upload it after blurring the person who didn't want to be in the video. With this software, this entire ordeal could be easily avoided.

# How do I use it?
It used to be running on an AWS server, but it is ridiculously expensive to keep up. If you want to try it yourself, just throw it all into your computer and edit the PHP script to call the python files where you have them. Yes, this is really convoluted, we're planning on making a version accessible to the end-user.

# What do we plan to change?
We plan to add a lot to this program, including the following:
+ Working GUI that works natively on Windows, Mac and Linux
+ Hardware acceleration to improve speed of processing
+ Custom algorithm to detect faces and license plates
+ General code cleanup
