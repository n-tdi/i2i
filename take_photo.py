import cv2
import BetterGlob as bg


def takePhoto(name, frame): # return a single frame in variable `frame`
    q = True
    while q:
        if "faces/"+name+".jpg" in bg.glob.glob("faces/"):
            name = name+"!"
        else:
            q = False
    cv2.imwrite(f'faces/{name}.jpg',frame)
    print("Photo taken")
