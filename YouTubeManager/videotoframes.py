import cv2
import os


def videotoframes(videoname, newfoldername=None):
    if newfoldername is None:
        newfoldername = videoname[:videoname.index('.')] + ' Frames' 
    os.mkdir(newfoldername)  #creates a folder to store extracted images
    print(cv2.__version__)  #current version is 4.6.0
    vidcap = cv2.VideoCapture(videoname)  #video needs to be in the same directory
    count = 1
    while True:
        success, image = vidcap.read()
        if not success:
            break
        # save frame as JPEG file
        cv2.imwrite(os.path.join(newfoldername, f"frame{count}.jpg"), image)
        count += 1
    print("{} images are extacted in {}.".format(count-1, newfoldername))


if __name__ == "__main__":
    videoname = "Upcoming Game _ _Black Rock Shooter FRAGMENT_ First Look Gameplay Trailer.mp4"
    videotoframes(videoname)
