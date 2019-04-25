import smtplib

def send_email(subject, to , msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login('logforyou.kjm@gmail.com', 'zfvliqmiwsmhieuj')
        server.sendmail('logforyou.kjm@gmail.com', to, msg)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")

