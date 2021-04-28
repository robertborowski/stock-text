import psycopg2
from psycopg2 import Error

def select_all_database_table_names_function(connection_postgres, cursor):
  """Returns: Pulls all the table names from the database"""
  try:
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
    result_list = cursor.fetchall()
    return result_list
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Error: ", error)
      result_list = 'none'
      return result_list