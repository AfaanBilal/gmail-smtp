# 
#  GMail SMTP Script
#  (c) Afaan Bilal ( https://afaan.ml ) 
#

import sys
import os.path
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

# [START] Send mail -----------------------------------------------------|
def send_mail(user, pwd, send_to, subject, text, files=None):
    
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = send_to if type(send_to) is list else [send_to]

    msg = MIMEMultipart()
    msg['From'] = FROM
    msg['To'] = COMMASPACE.join(TO)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, msg.as_string())
        server.close()
        print('Successfully sent the email')
    except:
        print('Failed to send the email')
# [END] Send mail -------------------------------------------------------|

print("GMail SMTP SendMail")
print("(c) Afaan Bilal ( https://afaan.ml )\n")

accounts_file = 'accounts.txt'
data_file     = 'data.txt'

if not os.path.isfile(accounts_file):
    print("Error: The accounts.txt file (database) does not exist")
    input("Press any key to exit...")
    sys.exit() 

data_file = input('Data filename: ')

if not os.path.isfile(data_file):
    print('Error: The file: ' + data_file + ' (data file) does not exist')
    input("Press any key to exit...")
    sys.exit() 

email_addr = ""
email_pass = ""
email_to   = ""
subject    = ""
attachment = ""
body       = ""

line_num = 0
for line in open(data_file):
    line_num += 1
    ldata = line.split(':')
    
    if line_num < 6 and len(ldata) < 2:
        continue
    
    if line_num >= 6:
        body += line + "\n"
    elif ldata[0] == "SENDER":
        email_addr = ldata[1].rstrip('\n')
    elif ldata[0] == "RECEIVER":
        email_to   = ldata[1].rstrip('\n')
    elif ldata[0] == "SUBJECT":
        subject    = ldata[1].rstrip('\n')
    elif ldata[0] == "ATTACHMENT":
        attachment = ldata[1].rstrip('\n')
    

print("FROM      : " + email_addr)
print("TO        : " + email_to)
print("SUBJECT   : " + subject)
print("ATTACHMENT: " + attachment)

for line in open(accounts_file):
    data = line.split(':')
    if len(data) < 2:
        continue
    if email_addr == data[0]:
        email_pass = data[1]

if email_pass == "":
    print("Error: no such sender email in the database")
    input("Press any key to exit...")
    sys.exit()

input("Press any key to send the email...")
allAttachments = [attachment] if attachment != "" else []
send_mail(email_addr, email_pass, email_to, subject, body, allAttachments)
input("Press any key to exit...")
