import cv2
import os
# create a folder to store extracted images


def videotoframes(videoname, newfoldername=None):
    if newfoldername is None:
        newfoldername = videoname[:videoname.index('.')] + ' Frames'
    os.mkdir(newfoldername)
    print(cv2.__version__) # current version is 3.1.0
    vidcap = cv2.VideoCapture(videoname) # video needs to be in the same directory
    count = 0
    while True:
        success, image = vidcap.read()
        if not success:
            break
        # save frame as JPEG file
        cv2.imwrite(os.path.join(newfoldername, f"frame{count}.jpg"), image)
        count += 1
    print("{} images are extacted in {}.".format(count, newfoldername))
