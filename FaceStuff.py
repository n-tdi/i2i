import cv2
from deepface import DeepFace
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
print(cv2.data.haarcascades)
video_capture = cv2.VideoCapture(0)
import BetterGlob as bg

DIRECTORY = bg.getdirectb("FaceStuff.py")


def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    Foundaface = False
    for x in bg.glob.glob(DIRECTORY.replace("\\", "/")+"faces/*"):
        #print(x.replace("/", "\\").replace(DIRECTORY+"faces\\", ""))
        if not Foundaface:
            if find_face(x.replace("/", "\\").replace(DIRECTORY+"faces\\", "")):
                print(x.replace("/", "\\").replace(DIRECTORY+"faces\\", "").replace(".jpg", ""))
                Foundaface = True
    if not Foundaface:
        print("unknown")
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return faces

def find_face(face):
    #print(frame)
    try:
        result = DeepFace.verify(DIRECTORY+"frame.jpg", DIRECTORY+f"faces\\{face}")
        #print(result["verified"])
        return result["verified"]
    except Exception as e:
        #print (e)
        return False
    



while True:
    result, video_frame = video_capture.read()  # read frames from the video
    if result is False:
        break  # terminate the loop if the frame is not read successfully
    
    cv2.imwrite(f'{DIRECTORY}frame.jpg', video_frame)
    faces = detect_bounding_box(
        video_frame
    )  # use the function we created earlier to the video frame

    cv2.imshow(
        "Faces", video_frame#, cv2.imread("C:/Users/marsr/Documents/python_class/PythonCode/Shrimp Lock/faces/charlie.jpg")#, video_frame
    )  # display the processed frame in a window named "My Face Detection Project"

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()