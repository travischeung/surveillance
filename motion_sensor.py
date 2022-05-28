        
import RPi.GPIO as GPIO
import time
import smtplib

gmail_user = 'travis.cheung69@gmail.com'
gmail_password = 'your_password'

sent_from = gmail_user
to = ['travis.cheung98@gmail.com']
subject = 'intruder detected'
body = ''

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(2, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin

while True:
    i=GPIO.input(2)
    if i==0:                 #When output from motion sensor is LOW
        print ("No intruders"),i
        GPIO.output(3, 0)  #Turn OFF LED
        time.sleep(0.1)
    elif i==1:               #When output from motion sensor is HIGH
        print ("Intruder detected"),i
    # Email sending
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)
        time.sleep(0.1)

    