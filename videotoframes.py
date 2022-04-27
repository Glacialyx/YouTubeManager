import cv2
import os
# create a folder to store extracted images
folder = 'VideoName Frames'
os.mkdir(folder)
# use opencv to do the job
print(cv2.__version__) # my version is 3.1.0
vidcap = cv2.VideoCapture('VideoName.mp4') # video needs to be in the same directory
count = 0
while True:
    success, image = vidcap.read()
    if not success:
        break
    # save frame as JPEG file
    cv2.imwrite(os.path.join(folder, "frame{:d}.jpg".format(count)), image)
    count += 1
print("{} images are extacted in {}.".format(count+1, folder))
