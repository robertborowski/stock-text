import psycopg2
from psycopg2 import Error

def insert_reminder_phone_table_function(connection_postgres, cursor, uuid_reminder_phone, reminder_phone_timestamp, user_uuid, confirm_phone_token, twilio_sid):
  """Returns: inserts into database table when text is sent"""

  postgres_insert_query = """INSERT INTO verify_phone_reminders_sent_table (pk_uuid_reminder_phone, timestamp_reminder_sent, fk_uuid_sent_to, phone_token_sent, twilio_message_sid) VALUES (%s, %s, %s, %s, %s)"""
  record_to_insert = (uuid_reminder_phone, reminder_phone_timestamp, user_uuid, confirm_phone_token, twilio_sid)
  
  try:
    cursor.execute(postgres_insert_query, record_to_insert)
    connection_postgres.commit()
    output_message = 'Success!'
    return output_message
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Error: ", error)
      output_message = 'Insert not successful.'
      return output_message