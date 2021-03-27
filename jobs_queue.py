from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.db.queries.select_queries.select_job_get_company_short_name import select_job_get_company_short_name_function
from backend.utils.yfinance.get_company_short_name import get_company_short_name_function
from backend.db.queries.insert_queries.insert_stock_news_links_table_company_short_name import insert_stock_news_links_table_company_short_name_function
from backend.utils.google_news.get_google_news_page import get_google_news_page_function
from backend.db.queries.update_queries.update_stock_news_links_table_company_short_name import update_stock_news_links_table_company_short_name_function
from backend.db.queries.delete_queries.delete_job_company_short_name import delete_job_company_short_name_function

def jobs_queues_function():
  """Return: Should run in the background automatically at intervals"""
  # Connect to database
  connection_postgres, cursor = connect_to_postgres_function()
  
  # get_company_short_name job
  print('==============================================================')
  print('- - - - - - - - TESTING JOB START - - - - - - - - - -')

  job_name = 'get_company_short_name'
  symbols_to_get_company_short_name_arr = select_job_get_company_short_name_function(connection_postgres, cursor, job_name)
  print('- - - -')
  print(symbols_to_get_company_short_name_arr)
  print('- - - -')

  for sym in symbols_to_get_company_short_name_arr:
    print('- - - -')
    print(sym)
    print('- - - -')
    # Search yfinance for company short name
    try:
      sym_company_short_name = get_company_short_name_function(sym)
    # If company short name not found
    except:
      print(sym + ' : Company short name cannot be found, or it took too long to find')
      sym_company_short_name = 'none'
      pass
    # If company short name found/asigned
    if sym_company_short_name != 'none':
      try:
        output_message_insert_company_short_name = insert_stock_news_links_table_company_short_name_function(connection_postgres, cursor, sym_company_short_name)
        try:
          google_news_link_with_company_short_name = get_google_news_page_function(sym_company_short_name)
        except:
          google_news_link_with_company_short_name = 'none'
          pass
        if google_news_link_with_company_short_name != 'none':
          try:
            update_stock_news_links_table_company_short_name_function(connection_postgres, cursor, google_news_link_with_company_short_name)
          except:
            pass
      except:
        pass

      # Finally delete the symbol from the job table
      try:
        delete_job_company_short_name_function(connection_postgres, cursor, job_name, sym_company_short_name)
      except:
        pass

  # Close connection to database
  close_connection_cursor_to_database_function(connection_postgres, cursor)

  print('- - - - - - - - TESTING JOB END - - - - - - - - - -')
  print('==============================================================')

# Run the main program
if __name__ == "__main__":
  jobs_queues_function()