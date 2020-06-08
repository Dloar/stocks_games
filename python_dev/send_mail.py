###
import smtplib
import datetime
from python_dev.functions import getDailyChange, getConfigFile
from email.message import EmailMessage
import warnings
warnings.filterwarnings("ignore")


config_conn = getConfigFile()
daily_looser, daily_gainer, daily_result, percentage_change = getDailyChange()

# sending to multiple people
contacts = [config_conn.email_user[0]]
msg = EmailMessage()
msg['Subject'] = 'Update at ' + datetime.datetime.today().strftime('%Y-%m-%d')
msg['From'] = config_conn.email_user[0]
msg['To'] = ', '.join(contacts)

msg.add_alternative("""\
<!DOCTYPE html>
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       Please see the results.
    </p>
  </body>
</html>
""", subtype='html')
msg.add_attachment(daily_looser, subtype='html')
msg.add_attachment("""

""")
# msg.add_attachment('daily_result, percentage_change)
msg.add_attachment(daily_gainer, subtype='html')


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