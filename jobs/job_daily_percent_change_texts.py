from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.queries.select_queries.select_all_stock_tracking_info import select_all_stock_tracking_info_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.utils.constant_run.invert_to_user_stocks_dict import invert_to_user_stocks_dict_function
from backend.utils.constant_run.get_unique_stocks_set import get_unique_stocks_set_function
from backend.utils.yfinance.get_latest_symbol_info import get_latest_symbol_info_function
from backend.db.queries.select_queries.select_all_user_phone_numbers import select_all_user_phone_numbers_function
from backend.utils.constant_run.invert_to_user_phone_numbers_dict import invert_to_user_phone_numbers_dict_function
from backend.utils.constant_run.create_queue_to_text_out import create_queue_to_text_out_function
from backend.utils.constant_run.twilio.send_sms import send_sms_function
from backend.utils.constant_run.twilio.send_summary_sms_text import send_summary_sms_text_function
from backend.db.queries.select_queries.select_all_google_news_links import select_all_google_news_links_function
from backend.utils.constant_run.create_news_links_dict import create_news_links_dict_function
import datetime

def pull_and_analyze_all_data_function():
  """Return: Should run in the background automatically at intervals"""

  # First check the day
  num_day_of_week = datetime.datetime.today().weekday()
  if num_day_of_week == 5 or num_day_of_week == 6:
    print('It is the weekend. The market is closed so texts do not go out on weekend!')
    return True

  # Connect to database
  connection_postgres, cursor = connect_to_postgres_function()

  # Pull data
  # Get all symbol tracking data from db
  all_data_symbol_track_arr_dicts = select_all_stock_tracking_info_function(connection_postgres, cursor)
  # Get all phone number data from db
  all_data_phone_numbers_arr_dicts = select_all_user_phone_numbers_function(connection_postgres, cursor)
  # Get all news link data from db
  all_news_links_arr = select_all_google_news_links_function(connection_postgres, cursor)
  
  # Close connection
  close_connection_cursor_to_database_function(connection_postgres, cursor)
  
  # Manipulate the pulled data into set & dicts
  unique_stocks_set = get_unique_stocks_set_function(all_data_symbol_track_arr_dicts)
  symbol_news_link_dict = create_news_links_dict_function(all_news_links_arr)
  user_stocks_tracking_dict = invert_to_user_stocks_dict_function(all_data_symbol_track_arr_dicts)
  user_phone_numbers_dict = invert_to_user_phone_numbers_dict_function(all_data_phone_numbers_arr_dicts)
  
  # Get yfinance information for the stock symbols as dict
  symbol_percent_changes_dict = get_latest_symbol_info_function(unique_stocks_set)
  
  # Put all the information together into a queue
  queue_to_text_arr = create_queue_to_text_out_function(user_stocks_tracking_dict, user_phone_numbers_dict, symbol_percent_changes_dict, symbol_news_link_dict)

  # Set variables for sending summary text to myself
  num_texts_to_send_out = len(queue_to_text_arr)
  num_texts_failed_to_send = 0

  # Open connection to database
  connection_postgres, cursor = connect_to_postgres_function()
  for i in queue_to_text_arr:
    try:
      send_sms_function(connection_postgres, cursor, i)
    except:
      num_texts_failed_to_send += 1
      pass

  # Send summary text to myself
  try:
    send_summary_sms_text_function(connection_postgres, cursor, num_texts_failed_to_send, num_texts_to_send_out)
  except:
    pass

  # Close connection to database
  close_connection_cursor_to_database_function(connection_postgres, cursor)

# Run the main program
if __name__ == "__main__":
  print('= = = = = = = = = = = = = = = = = JOB START (pull_and_analyze_all_data_function) = = = = = = = = = = = = = = = = =')
  pull_and_analyze_all_data_function()
  print('= = = = = = = = = = = = = = = = = JOB END (pull_and_analyze_all_data_function) = = = = = = = = = = = = = = = = =')