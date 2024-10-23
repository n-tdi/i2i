import cv2

cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 
ret,frame = cap.read() # return a single frame in variable `frame`

def takePhoto(name):
    ret,frame = cap.read() # return a single frame in variable `frame`
    cv2.imwrite('faces/${name}.jpg',frame)
    print("Photo taken")

def closeCamera():
    cap.release()