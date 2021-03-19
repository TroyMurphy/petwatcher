import smtplib, ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config

def send_mail_using_gmail(dogList):
	port = 587
	password = config('APP_PASSWORD', cast=str)

	if password is None:
		raise Exception("API Password not set")

	context = ssl.create_default_context()
	sender_email = "troymurphydev@gmail.com"
	receiver_email = config('EMAILTO', cast=str)

	with smtplib.SMTP(host='smtp.gmail.com', port=587) as s:
		s.ehlo()
		s.starttls()
		s.login("troymurphydev@gmail.com", password)
		# TODO: Send email here
		message = MIMEMultipart("alternative")
		message["Subject"] = "New pets on AARCS"
		message["From"] = sender_email
		message["To"] = receiver_email

		dogElems = [
			"""\
			<a href="{dog.link}">
				<h4>{dog.name}</h4>
				<img src="{dog.imageLink}"/>
			</a>
			<br/>
			""".format(dog=x) for x in dogList
		]
		html = """\
		<html>
			<body>
			<h1>{0} New Dogs Have Been Posted</h2>
				{1}
			</body>
		</html>
		""".format(len(dogList), "".join(dogElems))

		message.attach(MIMEText(html, "html"))
		s.sendmail(
			sender_email, receiver_email, message.as_string()
		)
