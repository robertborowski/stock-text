import os
from twilio.rest import Client
from backend.utils.create_uuid import create_uuid_function
from backend.utils.create_timestamp import create_timestamp_function
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.db.queries.insert_queries.insert_sent_texts_table import insert_sent_texts_table_function

def send_sms_function(connection_postgres, cursor, input_arr):
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

  message = client.messages.create(body=symbol + ' ' + percent_change + ' from previous close.\nLatest news articles for ' + symbol + ' here:\n' + google_link + '\n\nAdd symbols to news watchlist:\nSymbolNews.com',
                                  from_=os.environ.get('TWILIO_PHONE_NUMBER'),
                                  to=phone_number)
  print(message.sid)

  # Information that will go into the stock texts sent out table
  fk_uuid_user = input_arr[4]
  fk_uuid_symbol_track = input_arr[5]
  twilio_message_side = message.sid

  # Add the UUID and timestamp for datetime that the account was created
  user_uuid_text_sent = create_uuid_function("sndt_")
  user_timestamp_text_sent = create_timestamp_function()

  # Insert text message sent info into database
  sent_text_status = insert_sent_texts_table_function(connection_postgres, cursor, user_uuid_text_sent, user_timestamp_text_sent, fk_uuid_user, fk_uuid_symbol_track, twilio_message_side)
  print(sent_text_status)