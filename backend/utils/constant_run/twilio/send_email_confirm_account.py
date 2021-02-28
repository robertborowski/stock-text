import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

def send_email_confirm_account_function(to_email_address_outgoing, user_first_name, confirm_email_token):
  sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
  from_email = Email("noreply@symbolnews.com")  # Change to your verified sender
  to_email = To(to_email_address_outgoing)  # Change to your recipient
  subject = "Account Created - Verify Email"
  content = Content("text/plain", "Hi " + user_first_name + ",\n\n" + "Thank you for creating an account with SymbolNews!\n\n" + "Please click on the link below to verify your email address:\n" + "https://www.symbolnews.com/confirm/" + confirm_email_token + "\n\nBest,\nRob from SymbolNews")
  mail = Mail(from_email, to_email, subject, content)

  # Get a JSON-ready representation of the Mail object
  mail_json = mail.get()

  # Send an HTTP POST request to /mail/send
  #response = sg.client.mail.send.post(request_body=mail_json)