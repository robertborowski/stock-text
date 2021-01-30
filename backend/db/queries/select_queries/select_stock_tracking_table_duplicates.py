import bcrypt
import psycopg2
from psycopg2 import Error
def select_stock_tracking_table_duplicates_function(connection_postgres, cursor, uuid_to_search, symbol_to_search):
  """
  Returns: Looks if duplicate exists in the database table
  """
  try:
    cursor.execute("SELECT fk_user_uuid, symbol FROM stock_tracking_table WHERE fk_user_uuid=%s AND symbol=%s", [uuid_to_search, symbol_to_search])
    result_row = cursor.fetchone()
    if result_row != None:
      output_message = 'Already tracking this symbol for you.'
    else:
      output_message = 'none'
    return output_message
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Error: ", error)
      output_message = 'none'
      return output_message