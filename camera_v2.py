import cv2 as cv
import csv
from datetime import datetime
import time
import io
import picamera
import numpy
import pyzbar.pyzbar as pyzbar

# The purpose of this function is to scan qr code.....
def scan():
    def decode(img):
        decodedObjects = pyzbar.decode(img)
        # print(decodedObjects)
        for obj in decodedObjects:
            # print("Type: ", obj.type)
            # print("Data: ",obj.data,'\n')
            return (obj.data.decode('utf-8'))

    
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
            result = decode(image)
            if result != None:
                return result



# the purpose of this function is to change the encoding of the rows from csv file from utf-8 to ascii..
def convert_row( row ):
    row_dict = {}
    for key, value in row.items():
        keyAscii = key.encode('ascii', 'ignore' ).decode()
        valueAscii = value.encode('ascii','ignore').decode()
        row_dict[ keyAscii ] = valueAscii
    return row_dict

# The purpose of this function is to verify the scanned UID with the existing database..
def verify(uid):   
    details = {}
    with open("database.csv",mode="r") as database:
        reader = csv.DictReader(database)
        for row in reader:
            row  = convert_row(row)
            if (row['uid'] == uid):
                details['name'] = row['name']
                details['uid'] = uid
                details['roll no'] = row['roll_no']
                details['email'] = row['email']
                details['verification status'] = True
                return details
        else:
            details['verification status'] = False
        
    return details

# The purpose of this function is to detect the face and store the image in the current working directory..
def face_detect():


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
        image = cv.imdecode(buff, 1)
        stream.truncate(0)
        #Load a cascade file for detecting faces
        face_cascade = cv.CascadeClassifier('haar_cascades.xml')

        #Convert to grayscale
        gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)

        #Look for faces in the image using the loaded cascade file
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        print ("Found {} " + str(len(faces)) + " face(s)")
        if len(faces) !=0:
            cv.imwrite('DetectedImage.jpg',image)
            return (True,'DetectedImage.jpg')
        





# The purpose of this function is to get the current date and time.....
def getDateAndTime():  
    today = datetime.now()
    today = today.strftime("%d/%m/%Y %H:%M:%S")    
    date_time = {'date':today.split(' ')[0],'time': today.split(" ")[1]}
    # print(date_time)
    return date_time

# The purpose of this function is to log the attendance in the separate excel sheet locally...
def logInTime(details):
    with open("log.csv", mode = "a", newline="\n") as file:
        keys = ['date','name','status','uid','roll no','in time','out time']
        writer = csv.DictWriter(file,keys,delimiter = ",")
        # assuming that the file already has the headers so I'm leaving the part of assigning them..
        dateAndTime = getDateAndTime()
        date = dateAndTime['date']
        time_now = dateAndTime['time']
        values = {'date':date,'name':details['name'],'status':'in','uid':details['uid'],'roll no': details['roll no'],'in time':time_now,'out time':""}
        writer.writerow(values)
        return (date,time_now)       #returning entry time and date for email use

# The purpose of this function is to update the status and assign out time for the user...
def logOutTime(uid):
    temp = []  # temp array to copy the data and rewriting them in the same file with the updation of out time....
    with open('log.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if ((row['status'] == 'in') & (row['uid'] == uid)):
                row['status'] = 'out'
                dateAndTime = getDateAndTime()
                date = dateAndTime['date']
                time_now = dateAndTime['time']
                row['out time'] = time_now     
                temp.append(row)
                
            else:
                temp.append(row)
    with open("log.csv",mode="w", newline="\n") as file:
        keys = ['date','name','status','uid','roll no','in time','out time']
        writer = csv.DictWriter(file, fieldnames=keys, delimiter = ",")
        writer.writeheader()
        writer.writerows(temp)
    return(date,time_now)       #returning exit time and date for email use


def check_status(uid):
    with open('log.csv', mode='r') as file:
        ct = 0
        reader = csv.DictReader(file)
        for row in reader:
            if row['uid'] == uid:
                ct += 1
                if row['status'] == 'in':
                    return True

        else:
            return False

# read data continuously from Ultrasonic sensor 
# once the distance becomes less trigger scan function
# msg in lcd
# if qr code is scanned successfully then verify the qr code
# msg in lcd
# After verification take the photo of the user
# msg in lcd
# log in time in the csv file if the user enters the club for the first time..
# msg in lcd
# send mail
# log the out time in the csv file once the user leaves the club
# msg in lcd
# send mail


# Main code

