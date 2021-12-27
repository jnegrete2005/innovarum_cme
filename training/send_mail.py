from email.message import EmailMessage
import os
import smtplib
import re

EMAIL_ADDRESS = os.environ.get('AUTO_EMAIL')
EMAIL_PASSWORD = os.environ.get('AUTO_EMAIL_PASS')


def send_mail(to: str, message: str, subject: str):
  # TODO: change to pablo's email with env var
  contacts = [to, 'joaquin.negrete03@gmail.com']

  msg = EmailMessage()
  msg['Subject'] = subject
  msg['From'] = EMAIL_ADDRESS
  msg['To'] = ', '.join(contacts)
  msg.set_content(message)

  with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)


def check_email(email: str):
  regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

  if (re.search(regex, email)):
    return True

  return False
