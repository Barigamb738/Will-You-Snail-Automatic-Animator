import animator
import split
import cv2
import numpy as np
import os

projectName = "rickroll"
fullmp4Path = "2xrickroll.mp4"

if not os.path.isdir(projectName):
    os.mkdir(projectName)

split.split_by_seconds(fullmp4Path, 2.4, projectName)


videos = [f for f in os.listdir(projectName)]

print(videos)

for video in videos:
    animator.wysAnimate(60, video, projectName + "/" + video)
