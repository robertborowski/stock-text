import psycopg2
from psycopg2 import Error

def insert_sent_texts_table_function(connection_postgres, cursor, user_uuid_text_sent, user_timestamp_text_sent, fk_uuid_user, fk_uuid_symbol_track, twilio_message_side):
  """
  Returns: inserts into database table when user submits stock to track
  """
  postgres_insert_created_account_query = """INSERT INTO sent_texts_table(pk_uuid_sent_text, tracking_sent_text_date_time, fk_uuid_email, fk_uuid_symbol, twilio_message_sid) VALUES(%s,%s,%s,%s,%s)"""
  record_to_insert = (user_uuid_text_sent, user_timestamp_text_sent, fk_uuid_user, fk_uuid_symbol_track, twilio_message_side)
  try:
    cursor.execute(postgres_insert_created_account_query, record_to_insert)
    connection_postgres.commit()
    output_message = 'Successfully inserted to sent texts table!'
    return output_message
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Error: ", error)
      output_message = 'Insert not successful.'
      return output_message