import smtplib
from keys import gmpw


def send_email(to, subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login('logforyou.kjm@gmail.com', gmpw)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail('logforyou.kjm@gmail.com', to, message)
        server.quit()

    except Exception as err:
        print("Email failed to send.", err)