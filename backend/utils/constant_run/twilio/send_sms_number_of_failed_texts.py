import os
from twilio.rest import Client
from backend.utils.create_uuid import create_uuid_function
from backend.utils.create_timestamp import create_timestamp_function
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.db.queries.insert_queries.insert_sent_texts_table import insert_sent_texts_table_function

def send_sms_number_of_failed_texts_function(connection_postgres, cursor, num_texts_failed_to_send):
  """
  Returns: Send update text to user
  """
  phone_number = os.environ.get('PERSONAL_PHONE_NUMBER')
  print('- - - - - - - ')
  print(phone_number)
  print('- - - - - - - ')

  account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
  auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
  client = Client(account_sid, auth_token)

  message = client.messages.create(body=str(num_texts_failed_to_send) + ' texts failed to send today.',
                                  from_=os.environ.get('TWILIO_PHONE_NUMBER'),
                                  to=phone_number)
  print(message.sid)