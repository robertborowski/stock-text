import psycopg2
import psycopg2.extras
from psycopg2 import Error

def select_all_user_phone_numbers_function(connection_postgres, cursor):
  """
  Returns: All user phone numbers
  """
  try:
    # Add this to connection in order to pull data from postgres as a dictionary instead of tuple
    cursor = connection_postgres.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT uuid, phone_number FROM login_information_table WHERE confirmed_email=TRUE AND confirmed_phone_number=TRUE")
    result_arr = cursor.fetchall()
    result_arr_dicts = []
    for row in result_arr:
      result_arr_dicts.append(dict(row))
    return result_arr_dicts
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Status: ", error)
      return 'none'