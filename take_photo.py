import cv2
import BetterGlob as bg
cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 
ret,frame = cap.read() # return a single frame in variable `frame`

def takePhoto(name, dir):
    ret,frame = cap.read() # return a single frame in variable `frame`
    q = True
    while q:
        if dir+name+".jpg" in bg.glob.glob(dir):
            name = name+"!"
        else:
            q = False
    cv2.imwrite(f'faces/{name}.jpg',frame)
    print("Photo taken")

def closeCamera():
    cap.release()