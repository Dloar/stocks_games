###
import smtplib
import imghdr
from python_dev.functions import getConfigFile
from email.message import EmailMessage

config_conn = getConfigFile()

msg = EmailMessage()
msg['Subject'] = 'test1'
msg['From'] = config_conn.email_user[0]
msg['To'] = config_conn.email_user[0]
msg.set_content('Attachemnts in the mail.')

with open('heic1107a.jpg', 'rb') as f:
    file_data = f.read()
    file_type = imghdr.what(f.name)
    file_name = f.name

msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:  #Google connection SSL
    smtp.login(user=config_conn.email_user[0], password=config_conn.email_psw[0])

    smtp.send_message(msg=msg)




# with smtplib.SMTP('smtp.gmail.com', 587) as smtp:  #Google connection
#     smtp.ehlo()  # Initiate process
#     smtp.starttls()  # Encrypt
#     smtp.ehlo()  # Reinitiate process
#     subject = 'test1'
#     body = 'This is a body of the email'
#
#     msg = f'Subject: {subject}\n\n{body}'
#
#     smtp.sendmail(config_conn.email_user[0], 'deer923411@gmail.com', msg=msg)

# with smtplib.SMTP('localhost', 1025) as smtp:  #localhost connection
#     subject = 'test1'
#     body = 'This is a body of the email'
#
#     msg = f'Subject: {subject}\n\n{body}'
#
#     smtp.sendmail(config_conn.email_user[0], 'xkrao11@gmail.com', msg=msg)