
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

# Create a text/plain message
msg = email.mime.multipart.MIMEMultipart()
msg['Subject'] = '[Behatolás]'
msg['From'] = 'DjVajda@gmail.com'
msg['To'] = 'DjVajda@gmail.com'


gmail_user = 'DjVajda69@gmail.com'
gmail_password = 'Stupor69'
sent_from = gmail_user
#to = ['lomenarpad@gmail.com']
to =['detariandras@gmail.com']
#to =['dulacskamty@gmail.com']

# The main body is just another attachment
body = email.mime.text.MIMEText("Behatolás történt!")
msg.attach(body)


filename='valami.jpg'
fp=open(filename,'rb')
att = email.mime.application.MIMEApplication(fp.read(),_subtype="jpg")
fp.close()
att.add_header('Content-Disposition','attachment',filename=filename)
msg.attach(att)
'''
filename='valami2.gif'
fp=open(filename,'rb')
att = email.mime.application.MIMEApplication(fp.read(),_subtype="gif")
fp.close()
att.add_header('Content-Disposition','attachment',filename=filename)
msg.attach(att)
'''

# send via Gmail server
# NOTE: my ISP, Centurylink, seems to be automatically rewriting
# port 25 packets to be port 587 and it is trashing port 587 packets.
# So, I use the default port 25, but I authenticate
while(1):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, msg.as_string())
        server.close()
        print('Email sent!')
    except:
        print('Something went wrong...')












