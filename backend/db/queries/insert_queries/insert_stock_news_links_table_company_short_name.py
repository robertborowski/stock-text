import psycopg2
from psycopg2 import Error

def insert_stock_news_links_table_company_short_name_function(connection_postgres, cursor, company_short_name_input):
  """Returns: inserts into database table when user submits stock to track"""

  postgres_insert_query = """INSERT INTO stock_news_links_table (company_short_name) VALUES (%s)"""
  record_to_insert = (company_short_name_input)
  
  try:
    cursor.execute(postgres_insert_query, record_to_insert)
    connection_postgres.commit()
    output_message = 'Success!'
    return output_message
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Error: ", error)
      output_message = 'Insert not successful.'
      return output_message