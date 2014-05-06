'''
Created on Jan 19, 2014
A file provided for quick configuration of the connection to the SMTP-MTA server
@author: User
'''

# Common SMTP Connections (May be out of date. Search on google if that is the case)
# GMAIL
# SMTP_port = 587
# SMTP_host = 'smtp.gmail.com'
# SSL = False
#
# Yahoo
# SMTP_port = 465
# SMTP_host = 'smtp.mail.yahoo.com'
# SSL = True
#
# Outlook
# SMTP_port = 587
# SMTP_host = 'smtp.live.com'
# SSL = True
#
# AOL
# SMTP_port = 587
# SMTP_host = smtp.aol.com
# SSL = True

# The port where the SMTP Listener is active
SMTP_port = 587

# Set to host where your SMTP Listener is implemented
SMTP_host = 'smtp.gmail.com'

# If the SMTP connections is done over SSL, then set to true.
SSL = False

