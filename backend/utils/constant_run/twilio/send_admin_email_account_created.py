import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

def send_admin_email_account_created_function(user_first_name, user_last_name, user_email, created_timestamp):
  admin_email = os.environ.get('PERSONAL_EMAIL')
  sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
  from_email = Email(email = "robert@symbolnews.com", name = "Symbol News")  # Change to your verified sender
  to_email = To(admin_email)  # Change to your recipient
  subject = "Symbol News - Account Created"
  content = Content("text/plain", "Account Created\nFirst name: " + user_first_name + "\nLast name: " + user_last_name + "\nEmail: " + user_email + "\nCreated on: " + str(created_timestamp) + "\n\nBest,\nRob from Symbol News")
  mail = Mail(from_email, to_email, subject, content)

  # Get a JSON-ready representation of the Mail object
  mail_json = mail.get()

  # Send an HTTP POST request to /mail/send
  #response = sg.client.mail.send.post(request_body=mail_json)
  sg.client.mail.send.post(request_body=mail_json)