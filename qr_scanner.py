import io
import picamera
import cv2 as cv
import numpy
import time
import pyzbar.pyzbar as pyzbar

def decode(img):
    decodedObjects = pyzbar.decode(img)
    for obj in decodedObjects:
        print("Type: ", obj.type)
        print("Data: ",obj.data,'\n')
    if len(decodedObjects) !=0:
        return True
    else:
        return False

#Create a memory stream so photos doesn't need to be saved in a file
with picamera.PiCamera() as camera:
    while True:
    # camera.resolution = (320, 240)
        stream = io.BytesIO()
        time.sleep(1)
        camera.capture(stream, format='jpeg')

#Convert the picture into a numpy array
        buff = numpy.frombuffer(stream.getvalue(), dtype=numpy.uint8)
        stream.truncate(0)
#Now creates an OpenCV image
        image = cv.imdecode(buff, 1)
        decode(image)

#Save the result image
        cv.imwrite('result_qr.jpg',image)