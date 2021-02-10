from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.queries.select_queries.select_all_stock_tracking_info import select_all_stock_tracking_info_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
import time

def test_run_function():
  #-------------------------------
  """starttime = time.time()
  while True:
    print('tick')
    time.sleep(5.0 - ((time.time() - starttime) % 5.0))
    """
  #-------------------------------
  connection_postgres, cursor = connect_to_postgres_function()
  all_data_arr = select_all_stock_tracking_info_function(connection_postgres, cursor)
  close_connection_cursor_to_database_function(connection_postgres, cursor)
  print(all_data_arr)