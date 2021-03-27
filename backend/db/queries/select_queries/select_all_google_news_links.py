import psycopg2
import psycopg2.extras
from psycopg2 import Error

def select_all_google_news_links_function(connection_postgres, cursor):
  """
  Returns: Pulls all the info from the database
  """
  try:
    # Add this to connection in order to pull data from postgres as a dictionary instead of tuple
    cursor.execute("SELECT pk_symbol,google_news_link FROM stock_news_links_table")
    # Get the results arr
    result_arr = cursor.fetchall()

    # Return results
    return result_arr

  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Status: ", error)
      return 'none'