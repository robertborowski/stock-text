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
    cursor.execute("SELECT stock_tracking_table.symbol,stock_tracking_table.percent_change_to_notify,stock_tracking_table.fk_user_uuid,stock_tracking_table.uuid FROM stock_tracking_table LEFT JOIN login_information_table ON stock_tracking_table.fk_user_uuid=login_information_table.uuid WHERE login_information_table.confirmed_email=TRUE AND login_information_table.confirmed_phone_number=TRUE")
    # Get the results arr
    result_arr = cursor.fetchall()
    
    # Put results arr into dict
    result_arr_dicts = []
    for row in result_arr:
      result_arr_dicts.append(dict(row))
    
    # Retunr results dict
    return result_arr_dicts

  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Status: ", error)
      return 'none'