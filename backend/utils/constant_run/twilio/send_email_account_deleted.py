import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

def send_email_account_deleted_function(to_email_address_outgoing, user_first_name):
  sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
  from_email = Email("noreply@symbolnews.com")  # Change to your verified sender
  to_email = To(to_email_address_outgoing)  # Change to your recipient
  subject = "SymbolNews - Account Deleted"
  content = Content("text/plain", "Hi " + user_first_name + ",\n\n" + "Your SymbolNews account has been deleted." + "\n\nBest,\nRob from SymbolNews")
  mail = Mail(from_email, to_email, subject, content)

  # Get a JSON-ready representation of the Mail object
  mail_json = mail.get()

  # Send an HTTP POST request to /mail/send
  #response = sg.client.mail.send.post(request_body=mail_json)
  sg.client.mail.send.post(request_body=mail_json)