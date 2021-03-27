import psycopg2
from psycopg2 import Error

def insert_stock_news_links_table_function(connection_postgres, cursor, stock_symbol, google_news_url_link):
  """Returns: inserts into database table when user submits stock to track"""

  postgres_insert_created_account_query = """INSERT INTO stock_news_links_table (pk_symbol, google_news_link) VALUES (%s, %s)"""
  record_to_insert = (stock_symbol, google_news_url_link)
  
  try:
    cursor.execute(postgres_insert_created_account_query, record_to_insert)
    connection_postgres.commit()
    output_message = 'Success!'
    return output_message
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Error: ", error)
      output_message = 'Insert not successful.'
      return output_message