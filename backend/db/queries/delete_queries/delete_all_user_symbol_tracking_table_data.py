import psycopg2
from psycopg2 import Error

def delete_all_user_symbol_tracking_table_data_function(connection_postgres, cursor, uuid):
  """
  Returns: deletes all user symbols from table
  """
  try:
    cursor.execute("""DELETE FROM stock_tracking_table WHERE fk_user_uuid = %s;""", [uuid])
    connection_postgres.commit()
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Status: ", error)
  return True