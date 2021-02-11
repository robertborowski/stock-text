import psycopg2
import psycopg2.extras
from psycopg2 import Error

def select_all_stock_tracking_info_function(connection_postgres, cursor):
  """
  Returns: Pulls all the info from the database
  """
  try:
    # Add this to connection in order to pull data from postgres as a dictionary instead of tuple
    cursor = connection_postgres.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT symbol, percent_change_to_notify, fk_user_uuid FROM stock_tracking_table")
    result_arr = cursor.fetchall()
    result_arr_dicts = []
    for row in result_arr:
      result_arr_dicts.append(dict(row))
    return result_arr_dicts
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Status: ", error)
      return 'none'