import cv2

# take a photo
video_capture = None

x = 0
while True:
    video_capture = cv2.VideoCapture(x)
    if video_capture.read()[0]:
        break
    else:
        x+=1
print(x)

cv2.imwrite(f'test.jpg',video_capture.read()[1])
print("Photo taken")
