import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import lcd

def compose_mail(date_time,member_data,status,image):  #compose the email body
    if(status==False):                       #only read image while entering
        with open(image,'rb') as img:            #image from Pi Camera
            img_data = img.read()
    msg = MIMEMultipart()
    msg["Subject"] = "Reg: Entry to Robotics Club Lab"
    msg["From"] = "attendancerasp@gmail.com"
    msg["To"] = member_data["email"]

    body = "Dear {0}, (Roll No.-{1},RClub UID-{2}), \n\nSomeone has used your QR Code to  ".format(member_data["name"],member_data["roll no"],member_data["uid"])
    if(status):                               #specify whether entry or exit
        body += "Exit the Robotics Club Lab"
        body += " On {0} date at {1} time. ".format(date_time[0],date_time[1])
    else:
        body += "Enter the Robotics Club Lab"
        body += " On {0} date at {1} time. ".format(date_time[0],date_time[1])
        body += "We are sending a picture of the person who attempted login. Kindly verify \n\n"

    body_text = MIMEText(body)
    msg.attach(body_text)
    if(status==False):                     #only attach image on entry
        face = MIMEImage(img_data, name = image)     
        msg.attach(face)
    return msg.as_string()

    
def send_email(msg, to_addr): #code to send email
    from_addr = "attendancerasp@gmail.com"  ##RPi email ID
    pwd = "utlzftjhlhpqzysv"                    #email password
    server_url = "smtp.gmail.com"           
    ssl_port = 465
    context = ssl.create_default_context()
    print("Mail sent successfully")
    lcd.display("Mail sent\nsuccessfully")
    with smtplib.SMTP_SSL(server_url,ssl_port,context = context) as server:
        server.login(from_addr,pwd)
        server.sendmail(from_addr,to_addr,msg)
        server.quit()




    
        
                
    




