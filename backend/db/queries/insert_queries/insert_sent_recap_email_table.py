import psycopg2
from psycopg2 import Error
import json

def insert_sent_recap_email_table_function(connection_postgres, cursor, user_uuid_sent_email_recap, user_sent_email_recap_timestamp, user_uuid, mail_json, num_of_texts_this_week, symbols_sent_arr):
  """Returns: inserts into database table when user gets a recap email sent to them"""
  postgres_insert_query = """INSERT INTO sent_email_recap_table(pk_uuid_sent_email_recap, tracking_sent_email_recap_date_time, fk_uuid_email, email_recap_json, total_symbols_in_email, list_of_symbols_in_email) VALUES(%s,%s,%s,%s,%s,%s)"""
  record_to_insert = (user_uuid_sent_email_recap, user_sent_email_recap_timestamp, user_uuid, json.dumps(mail_json), num_of_texts_this_week, json.dumps(symbols_sent_arr))
  try:
    cursor.execute(postgres_insert_query, record_to_insert)
    connection_postgres.commit()
    output_message = 'Successfully inserted to sent texts table!'
    return output_message
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Error: ", error)
      output_message = 'Insert not successful.'
      return output_message