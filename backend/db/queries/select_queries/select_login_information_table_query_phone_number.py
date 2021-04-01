import psycopg2
from psycopg2 import Error

def select_login_information_table_query_phone_number_function(connection_postgres, cursor, phone_to_search):
  """Returns: if the email account already exists in database or not"""
  try:
    cursor.execute("SELECT phone_number FROM login_information_table WHERE phone_number=%s", [phone_to_search])
    result_row = cursor.fetchone()
    result_email = result_row[0]
    if result_email == phone_to_search:
      phone_exists = 'Account already exists'
      return phone_exists
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Status: Phone not taken, woohoo! ", error)
      phone_exists = 'none'
      return phone_exists