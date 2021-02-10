import psycopg2
from psycopg2 import Error

def select_all_stock_tracking_info_function(connection_postgres, cursor):
  """
  Returns: Pulls all the info from the database
  """
  try:
    cursor.execute("SELECT symbol, percent_change_to_notify, fk_user_uuid FROM stock_tracking_table")
    result_arr = cursor.fetchall()
    return result_arr
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Status: Email not taken, woohoo! ", error)
      return 'none'