import smtplib
from keys import pwd

def send_email(to, subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        pwd.encode('utf-8')
        email = 'logforyou.kjm@gmail.com'
        email.encode('utf-8')
        server.login(email, pwd)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        message.encode('utf-8')
        server.sendmail(email, to, message)
        server.quit()

    except Exception as err:
        print("Email failed to send.", err)

