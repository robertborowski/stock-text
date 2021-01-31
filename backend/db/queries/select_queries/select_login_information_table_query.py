import psycopg2
from psycopg2 import Error
def select_login_information_table_query_function(connection_postgres, cursor, email_to_search):
  """
  Returns: inserts into database when user creates an account
  """
  try:
    cursor.execute("SELECT email FROM login_information_table WHERE email=%s", [email_to_search])
    result_row = cursor.fetchone()
    result_email = result_row[0]
    if result_email == email_to_search:
      email_exists = 'Account already exists'
      return email_exists
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Status: Email not taken, woohoo! ", error)
      email_exists = 'none'
      return email_exists