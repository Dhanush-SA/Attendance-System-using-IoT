import io
import picamera
import cv2
import numpy
import time

#Create a memory stream so photos doesn't need to be saved in a file
while True:
    stream = io.BytesIO()

    #Get the picture (low resolution, so it should be quite fast)
    #Here you can also specify other parameters (e.g.:rotate the image)
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        time.sleep(2)
        camera.capture(stream, format='jpeg')

    #Convert the picture into a numpy array
    buff = numpy.frombuffer(stream.getvalue(), dtype=numpy.uint8)

    #Now creates an OpenCV image
    image = cv2.imdecode(buff, 1)
    stream.truncate(0)
    #Load a cascade file for detecting faces
    face_cascade = cv2.CascadeClassifier('haar_cascades.xml')

    #Convert to grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    #Look for faces in the image using the loaded cascade file
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    print ("Found {} " + str(len(faces)) + " face(s)")
    if len(faces) !=0:
        cv2.imwrite('DetectedImage.jpg',image)
        return (True,'DetectedImage.jpg')
        



