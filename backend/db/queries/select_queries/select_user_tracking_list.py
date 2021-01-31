import psycopg2
from psycopg2 import Error
def select_user_tracking_list_function(connection_postgres, cursor, uuid_to_search):
  """
  Returns: Looks if duplicate exists in the database table
  """
  try:
    cursor.execute("SELECT symbol, percent_change_to_notify FROM stock_tracking_table WHERE fk_user_uuid=%s", [uuid_to_search])
    result_list = cursor.fetchall()
    return result_list
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Error: ", error)
      result_list = 'none'
      return result_list