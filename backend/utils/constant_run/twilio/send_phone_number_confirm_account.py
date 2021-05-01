import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
from twilio.rest import Client

def send_phone_number_confirm_account_function(to_phone_number_outgoing, user_first_name, confirm_phone_token):
  """
  Returns: Send update text to user
  """
  phone_number = '1' + to_phone_number_outgoing
  
  account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
  auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
  client = Client(account_sid, auth_token)

  message = client.messages.create(body="Hi " + user_first_name + ",\n" + "Thank you for creating an account with Symbol News!\n" + "Please click on the link below to verify your phone number:\n" + "https://symbolnews.com/confirm/phone/" + confirm_phone_token + "\n\nBest,\nRob from Symbol News",
                                  from_=os.environ.get('TWILIO_PHONE_NUMBER'),
                                  to=phone_number)
  print(message.sid)