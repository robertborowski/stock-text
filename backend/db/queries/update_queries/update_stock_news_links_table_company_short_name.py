import psycopg2
import psycopg2.extras
from psycopg2 import Error

def update_stock_news_links_table_company_short_name_function(connection_postgres, cursor, new_google_news_link_with_company_short_name):
  """
  Returns: Updates the data in user database
  """
  try:
    cursor.execute("UPDATE stock_news_links_table SET google_news_link=%s", [new_google_news_link_with_company_short_name])
    connection_postgres.commit()
    print('Updated Information')
    #return 'Updated Information'
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Status: ", error)
      #return 'none'