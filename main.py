import RPi.GPIO as GPIO
import camera
import time
import email_sender
import lcd
import os
TRIG=21
ECHO=20
buzzer=3
GPIO.setmode(GPIO.BCM)
threshold=100

def start_operation():
        '''scan your qr'''
        authorization = False
        print("Scan your QR code")
        lcd.display("Scan your QRcode")
        uid = camera.scan()
        '''buzzer'''
        if (uid != None):
            ''' qr code scanned successfully'''
            print('qr code scanned successfully')
            lcd.display("Qr code scanned \n successfully")
            details = camera.verify(uid)
            if (details['verification status'] == False):
                '''unauthorized user'''
                print("unauthorized user")
                lcd.display("Unauthorized user")
                return authorization

            else:
                authorization = True
                status = camera.check_status(uid)
                img_loc = None
                if status == False:
                    _,img_loc=camera.face_detect()
                    (date,time_now)=camera.logInTime(details)
                    '''attendance casted successfully'''
                    print('attendance casted successfully - In Time')
                    lcd.display("In time casted\nSuccessfully")
                    '''mail'''

                elif status == True:
                    (date,time_now)=camera.logOutTime(uid)
                    '''Out time casted successfully'''
                    print("out time caseted succesfully")
                    lcd.display("out time casted\nsuccessfully")
                    '''mail'''
                msg_content = email_sender.compose_mail((date,time_now),details,status,img_loc)
                email_sender.send_email(msg_content,details["email"])
                if status == False:
                    os.remove(img_loc)
            return authorization
        else:
            return None  # it returns None if qr code is not scanned for a long time...


try:
    while True:
            # print("distance measurement in progress")
            GPIO.setup(TRIG,GPIO.OUT) #setting trigger pin as output
            GPIO.setup(ECHO,GPIO.IN)  #setting echo pin as input
            GPIO.setup(buzzer,GPIO.OUT)
            GPIO.output(buzzer,False)
            GPIO.output(TRIG,False)   #first keeping trigger pin as low
            time.sleep(0.2) #"waiting for sensor to settle"
            GPIO.output(TRIG,True)  #making trigger high to send pulse
            time.sleep(0.00001) # keeping trigger pin high for 10ms 
            GPIO.output(TRIG,False)
            while GPIO.input(ECHO)==0: #checking while echo is low 
                pulse_start=time.time() #measuring the start time when the pulse is being sent from trigger
            while GPIO.input(ECHO)==1: #checking while echo is high
                pulse_end=time.time() #measuring the end time when the oulse is being received
            pulse_duration=pulse_end-pulse_start #total time durarion of the pulse 
            distance=pulse_duration*17150 #distance in cm between the obstacle and the sensor
            distance=round(distance,2)
            # print("distance:",distance,"cm")
            if(distance<=threshold): #checking the distance is within the range
                GPIO.output(buzzer,True)
                time.sleep(1)
                GPIO.output(buzzer,False)

                authorization = start_operation()
                # if (authorization == True):
                #     '''Success... Now you can enter into the lab'''
                #     print("Success... Now you can enter into the lab")
                # elif (authorization == False):
                #     '''authorization failed check you id card for validity'''
                #     print("unauthorized user....")
                # elif (authorization == None):
                #     '''Again restarted after a 10 seconds gap of inactivity..'''
                #     pass
            else:
                '''Please come in front of the system'''
                print('You are not in range.Please come infront of the system')
                lcd.display("Not in range\nCome closer")
                time.sleep(2) 

except KeyboardInterrupt:
    GPIO.cleanup()
'''
read data continuously from Ultrasonic sensor 
once the distance becomes less trigger scan function
msg in lcd
if qr code is scanned successfully then verify the qr code
msg in lcd
After verification take the photo of the user
msg in lcd
log in time in the csv file if the user enters the club for the first time..
msg in lcd
send mail
log the out time in the csv file once the user leaves the club
msg in lcd
send mail
'''