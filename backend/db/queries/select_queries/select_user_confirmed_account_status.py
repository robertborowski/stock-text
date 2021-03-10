import psycopg2
from psycopg2 import Error

def select_user_confirmed_account_status_function(connection_postgres, cursor, uuid_to_search):
  """
  Returns: Pulls all the symbols and percentages that the user is tracking
  """
  try:
    cursor.execute("SELECT confirmed_email,confirmed_phone_number FROM login_information_table WHERE uuid=%s", [uuid_to_search])
    result_row = cursor.fetchone()
    confirm_status_email = result_row[0]
    confirm_status_phone_number = result_row[1]
    return confirm_status_email, confirm_status_phone_number
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Error: ", error)
      confirm_status_email = None
      confirm_status_phone_number = None
      return confirm_status_email, confirm_status_phone_number