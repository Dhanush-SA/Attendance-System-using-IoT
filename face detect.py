from picamera import PiCamera
import time
import cv2 as cv
camera = PiCamera()
haar_cascades = cv.CascadeClassifier("haar_cascades.xml")

def detect_face(img):
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    face_rect = haar_cascades.detectMultiScale(gray,scaleFactor = 1.1, minNeighbors = 10)
    print(face_rect)
    for (x,y,w,z) in face_rect:
        cv.rectangle(img,(x,y),(x+w,y+z), (0,255,0),thickness = 2)
        return True
    return False


#main code
while True:
    camera.start_preview()
    time.sleep(2)
    camera.capture("capture.jpg")
    img = cv.imread('capture.jpg')
    status = detect_face(img)
    if (status == True):
        break
    camera.stop_preview()
