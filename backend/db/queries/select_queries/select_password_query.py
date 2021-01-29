import bcrypt
import psycopg2
from psycopg2 import Error
def select_password_query_function(connection_postgres, cursor, email_to_search, password_to_search):
  """
  Returns: inserts into database when user creates an account
  """
  try:
    cursor.execute("SELECT password, first_name, last_name, phone_number FROM login_information_table WHERE email=%s", [email_to_search])
    # Results as array
    result_row = cursor.fetchone()
    # Results assigned
    result_email = email_to_search
    result_first_name = result_row[1]
    result_last_name = result_row[2]
    result_phone_number = result_row[3]
    salted_password = result_row[0].encode('ascii')
    if bcrypt.checkpw(password_to_search.encode('utf-8'), salted_password):
      return result_email, result_first_name, result_last_name, result_phone_number
    else:
      result_email = 'none'
      result_first_name = 'none'
      result_last_name = 'none'
      result_phone_number = 'none'
  except (Exception, psycopg2.Error) as error :
    if(connection_postgres):
      print("ERROR: ", error)
      result_email = 'none'
      result_first_name = 'none'
      result_last_name = 'none'
      result_phone_number = 'none'
  finally:
    return result_email, result_first_name, result_last_name, result_phone_number