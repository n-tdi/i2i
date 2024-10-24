import cv2
from deepface import DeepFace
import threading
#face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#print(cv2.data.haarcascades)
#video_capture = cv2.VideoCapture(0)
import BetterGlob as bg

global faces
global foundfaces
global num
num= 0
foundfaces = []
global threads
threads = []
global directory
global face_classifier
global video_capture
def init():
    global directory 
    directory = bg.getdirectb("FaceStuff.py")
    print(directory)
    global face_classifier
    global video_capture
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    video_capture = cv2.VideoCapture(0)

init()

'''
def faceStuff(name):
    if find_face(name):
        foundfaces.append(name.replace(".jpg", ""))
    #exit()
'''

def faceStuff():
    try:
        dfs = DeepFace.find(
    img_path = directory+"frame.jpg",
    db_path = directory+"faces\\",
    )
        for x in dfs:
            foundfaces.append(x.to_dict()["identity"][0].replace(directory, "").replace("faces\\", "").replace(".jpg", "").replace("!", ""))
    except Exception as e:
        print("uh oh!")
        print(e)


def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    Foundaface = False
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
    if len(faces)>0:
        image = vid.copy()[faces[0][1]:faces[0][1]+faces[0][3], faces[0][0]:faces[0][0]+faces[0][2]]
        cv2.imwrite(f'{directory}frame.jpg', video_frame)
        #for x in bg.glob.glob(directory.replace("\\", "/")+"faces/*"):
        #    threads.append(f"Thread-{x}-{num}")
            #threading.Thread(None, faceStuff, f"Thread-{x}-{num}", args = (x.replace("/", "\\").replace(directory+"faces\\", ""), )).run()
        threading.Thread(None, faceStuff, f"Thread-{x}-{num}", args = ( )).run()

    return faces


def find_face(face):
    #print(frame)
    try:
        result = DeepFace.verify(directory+"frame.jpg", directory+f"faces\\{face}")
        #print(result["verified"])
        return result["verified"]
    except Exception as e:
        #print (e)
        return False
    


time = -1
while True:
    result, video_frame = video_capture.read()  # read frames from the video
    if result is False:
        break  # terminate the loop if the frame is not read successfully
    
    cv2.imwrite(f'{directory}frame.jpg', video_frame)
    time+=1

    if time%30 == 0:
        face = detect_bounding_box(
            video_frame
        )  # use the function we created earlier to the video frame

    if not foundfaces == []:
        print(foundfaces)
        foundfaces = []
    else:
        #print("searching...")
        #print(directory)
        pass
    cv2.imshow(
        "Faces", video_frame#, cv2.imread("C:/Users/marsr/Documents/python_class/PythonCode/Shrimp Lock/faces/charlie.jpg")#, video_frame
    )  # display the processed frame in a window named "My Face Detection Project"

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()