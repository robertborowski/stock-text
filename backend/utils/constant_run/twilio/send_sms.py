import os
from twilio.rest import Client

def send_sms_function(input_arr):
  """
  Returns: Send update text to user
  """
  phone_number = '1' + str(input_arr[0])
  symbol = input_arr[1]
  percent_change = input_arr[2]
  google_link = input_arr[3]
  
  account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
  auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
  client = Client(account_sid, auth_token)

  message = client.messages.create(body=symbol + ' ' + percent_change + ' from previous close.\n' + google_link + '\n\nSymbolNews',
                                  from_=os.environ.get('TWILIO_PHONE_NUMBER'),
                                  to=phone_number)
  #print(message.sid)