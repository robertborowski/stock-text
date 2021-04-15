import psycopg2
from psycopg2 import Error

def insert_reminder_email_table_function(connection_postgres, cursor, uuid_reminder_email, reminder_email_timestamp, user_uuid, confirm_email_token):
  """Returns: inserts into database table when user submits stock to track"""

  postgres_insert_query = """INSERT INTO verify_email_reminders_sent_table (pk_uuid_reminder_email, timestamp_reminder_sent, fk_uuid_sent_to, email_token_sent) VALUES (%s, %s, %s, %s)"""
  record_to_insert = (uuid_reminder_email, reminder_email_timestamp, user_uuid, confirm_email_token)
  
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