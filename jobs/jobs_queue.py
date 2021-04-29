from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.db.queries.select_queries.select_job_get_company_short_name import select_job_get_company_short_name_function
from backend.utils.yfinance.get_company_short_name import get_company_short_name_function
from backend.utils.google_news.get_google_news_page import get_google_news_page_function
from backend.db.queries.update_queries.update_stock_news_links_table_google_link import update_stock_news_links_table_google_link_function
from backend.db.queries.update_queries.update_stock_news_links_table_company_short_name import update_stock_news_links_table_company_short_name_function
from backend.db.queries.delete_queries.delete_job_company_short_name import delete_job_company_short_name_function

def jobs_queues_function():
  """Return: Should run in the background automatically at intervals"""
  # Connect to database
  connection_postgres, cursor = connect_to_postgres_function()
  
  # get_company_short_name job
  job_name = 'get_company_short_name'
  symbols_to_get_company_short_name_arr = select_job_get_company_short_name_function(connection_postgres, cursor, job_name)

  # Loop through all symbols in job
  for sym in symbols_to_get_company_short_name_arr:
    # Get company short name
    try:
      sym_company_short_name = get_company_short_name_function(sym[0])
    # If company short name not found
    except:
      print(sym[0] + ' : Company short name cannot be found, or it took too long to find')
      sym_company_short_name = 'none'
      pass
    
    # If company short name found/asigned
    if sym_company_short_name != 'none':
      try:
        # Update table with company short name
        update_stock_news_links_table_company_short_name_function(connection_postgres, cursor, sym_company_short_name, sym[0])
        # Get updated google link
        try:
          google_news_link_with_company_short_name = get_google_news_page_function(sym_company_short_name)
        except:
          google_news_link_with_company_short_name = 'none'
          pass
        
        # If Google news link with company short name has been found/created
        if google_news_link_with_company_short_name != 'none':
          try:
            update_stock_news_links_table_google_link_function(connection_postgres, cursor, google_news_link_with_company_short_name, sym[0])
          except:
            pass
      except:
        pass

      # Finally delete the symbol from the job table
      try:
        delete_job_company_short_name_function(connection_postgres, cursor, job_name, sym[0])
      except:
        pass

  # Close connection to database
  close_connection_cursor_to_database_function(connection_postgres, cursor)

# Run the main program
if __name__ == "__main__":
  print('= = = = = = = = = = = = = = = = = JOB START (jobs_queues_function) = = = = = = = = = = = = = = = = =')
  jobs_queues_function()
  print('= = = = = = = = = = = = = = = = = JOB END (jobs_queues_function) = = = = = = = = = = = = = = = = =')