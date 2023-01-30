
import smtplib
from email.mime.text import MIMEText

sender = 'pi@asfalis'
receivers = ['ermiasyemane91@gmail.com']


port = 25
msg = MIMEText('The Larm is Activated')

msg['Subject'] = 'Test mail'
msg['From'] = 'pi@asfalis'
msg['To'] = 'ermiasyemane91@gmail.com'

def send_Email():
    with smtplib.SMTP('localhost', port) as server:
    
    
        server.sendmail(sender, receivers, msg.as_string())
      