'''
Created on Jan 19, 2014

@author: Nathan
'''
import argparse

import os
from os import path

from EmailScriptUtilities import MyFlattener

import smtplib #, os
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from mimetypes import guess_type
from email.utils import COMMASPACE, formatdate
from email import encoders
import SMTPConfiguration

def send_mail(send_from, password, send_to, subject, text, files=[], host=SMTPConfiguration.SMTP_host, port=SMTPConfiguration.SMTP_port):
    """Using SMTP, this method sends an email with a subject, body, and attachments to the emails listed in send_to from the email in send_from"""
    
    assert type(send_to)==list
    assert type(files)==list
    
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime = True)
    msg['Subject'] = subject
    
    # The actual text of the email
    msg.attach( MIMEText(text) )
    
    # Attaching the attachments to the email message
    for f in files:
        mimetype, encoding = guess_type(f)
        mimetype = mimetype.split('/', 1)
        file_handle = open(f, 'rb')
        attachment = MIMEBase(mimetype[0], mimetype[1])
        attachment.set_payload(file_handle.read())
        file_handle.close()
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(f))
        msg.attach(attachment)        
        
    # Trying the connection to the SMTP server
    try:
        server = smtplib.SMTP(host, port)
        if SMTPConfiguration.SSL:
            server = smtplib.SMTP_SSL(host, port)
        server.ehlo
        server.starttls()
        server.login(send_from, password)
        server.sendmail(send_from, send_to, msg.as_string())
        server.close()
        print("Successfully sent the email")
    except SMTPException as error:
        print("Failed to send mail: {err}".format(err=error))

fltnr = MyFlattener()


# Setting up the command line argument parser
parser = argparse.ArgumentParser()
parser.add_argument('author', nargs=1, action='store', type=str, help='the email address sending the email')
parser.add_argument('password', nargs=1, action='store', help='the password of the email address sending the email')
parser.add_argument('to', nargs='+', action='append', help='list of addresses the email will be sent to')
parser.add_argument('-s', '--subject', action='store', type=str, nargs='*', required=False, help='the subject of the email', dest='subject')
parser.add_argument('-b', '--body', action='store', type=str, nargs='*', required=False, help='the body of the email', dest='body')
parser.add_argument('-f', '--files', action='append', nargs='*', required=False, help='list of files to be attached to email', dest='files')
parser.add_argument('-d', '--directories', action='append', nargs='*', required=False, help='list of directories where all files in directory will be attached', dest='directories')

# Massaging the arguments from the argument parser into nicer formats
args = parser.parse_args()
opts = vars(args)
author = opts.get('author')

if opts.get('subject') is None:
    subject = ['(no', 'subject)']
else:
    subject = opts.get('subject')
    
if opts.get('body') is None:
    body = ['No', 'message.']
else:
    body = opts.get('body')
files = []
if opts.get('files') is not None:
    files = fltnr.flatten_list_of_list(opts.get('files'))
directories = []
if opts.get('directories') is not None:
    directories = fltnr.flatten_list_of_list(opts.get('directories'))
to = fltnr.flatten_list_of_list(opts.get('to'))
password = opts.get('password')

# Printing for Debugging purposes
# print(author)
# print(password)
# print(to)
#print(subject)
#print(body)
# print(files)
# print(directories)

# List of files to be attached to email
file_list = []


for f in files:
    if path.isfile(f): # Note: file will not be valid if followed by slashes
        # Construct the full path name of the file
        dir_path = path.dirname(path.realpath(f))
        head, tail = path.split(f)

        # Add the full path of the file to the list of files to be attached
        file_list.extend([path.join(dir_path,tail)])
        
for d in directories:
    if path.isdir(d):
        # Construct the full path name of the directory d
        temp_path = path.realpath(d)
        
        # Adds every file in the top level of the directory d to the list of files to be attached 
        for (dirpath, dirnames, filenames) in os.walk(temp_path):
            file_list.extend(path.join(dirpath,filename) for filename  in filenames)
            break
#print(file_list)

# Remove duplicate from the list of files to be attached to the email. Does not preserve order
file_set = list(set(file_list))

#print(" ".join(str(x) for x in body))
#print(" ".join(str(x) for x in subject))


send_mail(fltnr.list_to_str(author, ""), fltnr.list_to_str(password, ""), to, fltnr.list_to_str(subject, " "), fltnr.list_to_str(body, " "), file_set)