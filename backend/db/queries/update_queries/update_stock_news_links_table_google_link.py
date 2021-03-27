import psycopg2
import psycopg2.extras
from psycopg2 import Error

def update_stock_news_links_table_google_link_function(connection_postgres, cursor, new_google_news_link_with_company_short_name, input_symbol):
  """
  Returns: Updates the data in user database
  """
  try:
    cursor.execute("UPDATE stock_news_links_table SET google_news_link=%s WHERE pk_symbol=%s", [new_google_news_link_with_company_short_name, input_symbol])
    connection_postgres.commit()
    print('Successfully updated information into table')
    #return 'Updated Information'
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Status: ", error)
      #return 'none'