import psycopg2
from psycopg2 import Error

def delete_from_stock_tracking_table_function(connection_postgres, cursor, uuid, symbols_arr):
  """
  Returns: inserts into database when user creates an account
  """
  for sym in symbols_arr:
    postgres_delete_symbols_query = """DELETE FROM stock_tracking_table WHERE fk_user_uuid = %s AND symbol = %s;"""
    record_to_delete = (uuid, sym)
    try:
      cursor.execute(postgres_delete_symbols_query, record_to_delete)
      connection_postgres.commit()
    except (Exception, psycopg2.Error) as error:
      if(connection_postgres):
        print("Status: ", error)
  return True