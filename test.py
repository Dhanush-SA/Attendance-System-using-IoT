import cv2 as cv
import csv
from datetime import datetime
import time

# The purpose of this function is to scan qr code.....
def scan():
    timeout = 100             # seconds  # to stop scanning after 10 seconds of inactivity
    triggered_time = time.time()
    uid = ""
    scanned = False
    cap = cv.VideoCapture(0)
    detector = cv.QRCodeDetector()
    print("Reading qr code using raspberry pi")

    while scanned == False:
        if (time.time()<triggered_time+timeout):
            isTrue, frame = cap.read()
            data,bbox,retr = detector.detectAndDecode(frame)
            cv.imshow("video",frame)
            if bbox is not None:
                if data:
                    print("Data found "+data)
                    uid = data
                    scanned=True
                    cap.release()
                    cv.destroyAllWindows()
                    return uid
            if cv.waitKey(20) & 0xFF == ord('d'):
                break
        else:
            return 


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
    haar_cascades = cv.CascadeClassifier("haar_cascades.xml")
    # The purpose of this function is to detect any faces that are appearing in front of the camera...
    def detect_face(img):
        gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        face_rect = haar_cascades.detectMultiScale(gray,scaleFactor = 1.1, minNeighbors = 10)
        if len(face_rect) == 1:
            return True
        return False

    video = cv.VideoCapture(0)
    count = 0
    while count != 2:
        isTrue, frames = video.read()
        cv.imshow("video",frames)
        if (detect_face(frames)):
            time.sleep(0.5)
            count += 1    # here i'm waiting for the next to frames to get a clear image without any noises..
            if (count == 2):
                cv.imwrite("DetectedImage.jpg",frames)  # saving the image....
                return (True,"DetectedImage.jpg")   # It return true after the successful detection of face detection
                #returning image location also for email attachment
        if cv.waitKey(20) & 0xFF == ord('d'):
            break
    video.release()
    video.destroyAllWindows()

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

