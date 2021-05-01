import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

def send_email_new_password_function(to_email_address_outgoing, confirm_email_token):
  sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
  from_email = Email(email = "robert@symbolnews.com", name = "Symbol News")  # Change to your verified sender
  to_email = To(to_email_address_outgoing)  # Change to your recipient
  subject = "Symbol News - Forgot Password - New Password Link"
  content = Content("text/plain", "Hi " + to_email_address_outgoing + ",\n\n" + "Password reset link:\n" + "https://symbolnews.com/set_new_password/" + confirm_email_token + "\n\nBest,\nRob from Symbol News")
  mail = Mail(from_email, to_email, subject, content)

  # Get a JSON-ready representation of the Mail object
  mail_json = mail.get()

  # Send an HTTP POST request to /mail/send
  #response = sg.client.mail.send.post(request_body=mail_json)
  sg.client.mail.send.post(request_body=mail_json)