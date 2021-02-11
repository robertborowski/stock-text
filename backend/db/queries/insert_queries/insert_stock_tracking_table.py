import psycopg2
from psycopg2 import Error
def insert_stock_tracking_table_function(connection_postgres, cursor, uuid, submission_timestamp, stock_symbol, percent_change_to_notify, fk_user_uuid, google_news_url_link):
  """
  Returns: inserts into database table when user submits stock to track
  """
  postgres_insert_created_account_query = """INSERT INTO stock_tracking_table (uuid, tracking_submission_date, symbol, percent_change_to_notify, fk_user_uuid, google_news_link) VALUES (%s, %s, %s, %s, %s, %s)"""
  record_to_insert = (uuid, submission_timestamp, stock_symbol, percent_change_to_notify, fk_user_uuid, google_news_url_link)
  try:
    cursor.execute(postgres_insert_created_account_query, record_to_insert)
    connection_postgres.commit()
    output_message = 'Success!'
    return output_message
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Error: ", error)
      output_message = 'Insert not successful.'
      return output_message