import psycopg2
from psycopg2 import Error

def close_connection_cursor_to_database_function(connection_postgres, cursor):
  """
  Returns: Closes the connections to postgres
  """
  cursor.close()
  connection_postgres.close()
  print('CONNECTION AND CURSOR ARE CLOSED')