import sys
sys.path.append("/usr/local/lib/python3.5/dist-packages")
sys.path.append("/usr/lib/python3/dist-packages")
sys.path.append("/home/pi/.local/lib/python2.7/site-packages")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
# Import smtplib for the actual sending function
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# For guessing MIME type
import mimetypes
import email.mime.application
# Import the email modules we'll need
import email
import email.mime
import timeit
import time

class EmailSend(object):
    def __init__(self):
        self.msg = email.mime.multipart.MIMEMultipart()
        self.msg['Subject'] = '[Behatolás]'
        self.msg['From'] = 'DjVajda@gmail.com'
        self.msg['To'] = "DjVajda@gmail.com"
        self.gmail_user = 'DjVajda69@gmail.com'
        self.gmail_password = 'Stupor69'
        self.sent_from = self.gmail_user
        self.body = email.mime.text.MIMEText("Behatolás történt!")
        self.msg.attach(self.body)
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
     
    def Send(self,to,img):
        try:
            '''
            filename='valami.jpg'
            fp=open(filename,'rb')
            att = email.mime.application.MIMEApplication(fp.read(),_subtype="jpg")
            fp.close()
            att.add_header('Content-Disposition','attachment',filename=filename)
            self.msg.attach(att)
            '''
                
            filename='detected.jpg'
            att = email.mime.application.MIMEApplication(img,_subtype="jpg")
            att.add_header('Content-Disposition','attachment',filename=filename)
            self.msg.attach(att)
            
            self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            self.server.ehlo()
            self.server.login(self.gmail_user, self.gmail_password)
              
            self.server.sendmail(self.sent_from,to, self.msg.as_string())
            self.server.close()
            print('Email sent!')
        except:
            print('Something went wrong...')
    def SetAdress(self,address):
         self.msg['To'] = adress
'''
EmailClass=MyMail()
to =['detariandras@gmail.com','DjVajda@gmail.com']
while(1):
    EmailClass.Send(to)
    time.sleep(1)
'''    
    
    
    
    
    
                
        
        
        
        
        
        
        
        