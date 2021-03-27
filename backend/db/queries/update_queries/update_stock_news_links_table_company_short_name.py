import psycopg2
import psycopg2.extras
from psycopg2 import Error

def update_stock_news_links_table_company_short_name_function(connection_postgres, cursor, company_short_name_input, symbol_input):
  """
  Returns: Updates the data in user database
  """
  try:
    cursor.execute("UPDATE stock_news_links_table SET company_short_name=%s WHERE pk_symbol=%s", [company_short_name_input, symbol_input])
    connection_postgres.commit()
    print('Successfully updated company short name information into table')
    #return 'Updated Information'
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Status: ", error)
      #return 'none'