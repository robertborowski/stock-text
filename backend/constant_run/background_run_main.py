from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.queries.select_queries.select_all_stock_tracking_info import select_all_stock_tracking_info_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.utils.constant_run.invert_to_user_stocks_dict import invert_to_user_stocks_dict_function
from backend.utils.constant_run.get_unique_stocks_set import get_unique_stocks_set_function
from backend.utils.yfinance.get_latest_symbol_info import get_latest_symbol_info_function

def pretty(d, indent=0):
  for key, value in d.items():
    print('\t' * indent + str(key))
    if isinstance(value, dict):
      pretty(value, indent+1)
    else:
      print('\t' * (indent+1) + str(value))

def pull_and_analyze_all_data_function():
  """
  Return: user stock dict
  """
  # Get all data from db
  connection_postgres, cursor = connect_to_postgres_function()
  all_data_arr_dicts = select_all_stock_tracking_info_function(connection_postgres, cursor)
  close_connection_cursor_to_database_function(connection_postgres, cursor)
  # Manipulate the pulled data
  unique_stocks_set = get_unique_stocks_set_function(all_data_arr_dicts)
  user_stocks_tracking_dict = invert_to_user_stocks_dict_function(all_data_arr_dicts)
  # Get outside information for the stock symbols
  symbol_lookup_dict = get_latest_symbol_info_function(unique_stocks_set)