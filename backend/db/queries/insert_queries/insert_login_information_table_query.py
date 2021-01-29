import psycopg2
from psycopg2 import Error
def insert_login_information_table_query_function(connection_postgres, cursor, uuid, timestamp, first_name, last_name, phone_number, email, hashed_password):
  """
  Returns: inserts into database when user creates an account
  """
  postgres_insert_created_account_query = """INSERT INTO login_information_table (uuid, account_created_date, first_name, last_name, phone_number, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
  record_to_insert = (uuid, timestamp, first_name, last_name, phone_number, email, hashed_password)
  try:
    cursor.execute(postgres_insert_created_account_query, record_to_insert)
    connection_postgres.commit()
    success_message = 'success'
    error_message = 'none'
    return success_message, error_message
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Status: Email not taken - ", error)
      success_message = 'none'
      error_message = 'Account already exists.'
      return success_message, error_message