import psycopg2
from psycopg2 import Error

def delete_all_user_login_information_table_data_function(connection_postgres, cursor, uuid):
  """
  Returns: deletes all user symbols from table
  """
  try:
    cursor.execute("""DELETE FROM login_information_table WHERE uuid = %s;""", [uuid])
    connection_postgres.commit()
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Status: ", error)
  return True