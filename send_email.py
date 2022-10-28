from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from locale import locale_alias
import smtplib
import mimetypes
from email import encoders

my_email = "coffeedatadev@gmail.com"
receiveEmail = "coffeedatadev@gmail.com"
my_password = "rdeygcxvmwyldvyo"

message = MIMEMultipart()
message['From'] = my_email
message['To'] = receiveEmail
message['Subject'] = 'Here is your Weekly EPL Roundup'


standingsFile = 'eplFullStandings.csv'
matchFile = 'eplMatchweek.csv'

attachment = open(standingsFile, 'rb')
attachment2 = open(matchFile, 'rb')

obj = MIMEBase('application', 'octet-stream')
obj.set_payload((attachment).read())
encoders.encode_base64(obj)
obj.add_header('Content-Disposition',"attachment; filename= "+standingsFile)

obj2 = MIMEBase('application', 'octet-stream')
obj2.set_payload((attachment2).read())
encoders.encode_base64(obj2)
obj2.add_header('Content-Disposition',"attachment; filename= "+matchFile)

message.attach(obj)
message.attach(obj2)

my_message = message.as_string()

with smtplib.SMTP("smtp.gmail.com", 587) as connection:
    connection.starttls()
    connection.login(my_email, my_password)
    connection.sendmail(
        from_addr=my_email,
        to_addrs=receiveEmail,
        msg=my_message
    )
