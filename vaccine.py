import json
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.header import Header
from email.MIMEText import MIMEText
from email.utils import formataddr
import json
import datetime
import requests
from bs4 import BeautifulSoup
import hashlib
import os.path



# def lambda_handler(event, context):
def myFunction():
		 
	#Enter email information
	fromaddr = ""
	password = ""
	toaddr = ['myemail']

	displayName = 'Vaccine Master'
	
	
	msg = MIMEMultipart('alternative')
	msg['From'] = formataddr((str(Header(displayName, 'utf-8')), fromaddr))
	
	
	#Edit subject, message, and reply-to information here
	msg['Subject'] = "Vaccine Website Update"
	msg['To'] = ",".join(toaddr)


	headers = {'User-Agent': 'Mozilla/5.0'}
	requests.packages.urllib3.disable_warnings()
	r = requests.get('https://www.rivcoph.org/COVID-19-Vaccine', headers=headers, verify=False)

	soup = BeautifulSoup(r.text,features="html.parser")
	container = soup.find(id = 'dnn_ctr2947_ContentPane')

	currentHash = hashlib.sha224(str(container)).hexdigest()

	if os.path.isfile("hash.txt"):
		f = open("hash.txt", "r")
		previousHash = f.readline()
		f.close()
		if (previousHash == currentHash):
			return

	f = open("hash.txt", "w")
	f.write(currentHash)
	f.close()

	table = str(container)
	table = table.replace("/portals/0/Images/coronavirus/testing/", "https://www.rivcoph.org/portals/0/Images/coronavirus/testing/")

	msg.attach(MIMEText(table, 'plain'))


	htmlBegin = """
	<html>
	  <head></head>
	  <body>
	 	https://www.rivcoph.org/COVID-19-Vaccine
	"""
	htmlEnd = """
	  </body>
	</html>
	"""
	
	html = MIMEText(htmlBegin + table + htmlEnd, 'html')
	msg.attach(html)


	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, password)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

myFunction()
