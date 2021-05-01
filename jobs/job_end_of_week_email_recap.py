from flask import Flask, redirect, url_for, request, session, Blueprint
import datetime
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.db.queries.select_queries.select_users_received_text_this_week import select_users_received_text_this_week_function
from backend.utils.constant_run.convert_arr_dict_texts_this_week import convert_arr_dict_texts_this_week_function
from backend.db.queries.select_queries.select_users_received_text_this_week_symbols_only import select_users_received_text_this_week_symbols_only_function
from backend.utils.constant_run.convert_arr_dict_symbols_this_week_with_change import convert_arr_dict_symbols_this_week_with_change_function
from backend.utils.constant_run.twilio.send_email_weekly_recap_sym_thresholds import send_email_weekly_recap_sym_thresholds_function

def job_end_of_week_email_recap_function():
  """Pulls all users who recieved texts this week then sends them an end of week recap, with news links"""
  # First check the day
  num_day_of_week = datetime.datetime.today().weekday()
  if num_day_of_week == 0 or num_day_of_week == 1 or num_day_of_week == 2 or num_day_of_week == 3 or num_day_of_week == 5 or num_day_of_week == 6:
    return True

  if num_day_of_week == 4:
    # Connect to database
    connection_postgres, cursor = connect_to_postgres_function()

    # Pull user data who received texts this week
    texts_this_week_arr = select_users_received_text_this_week_function(connection_postgres, cursor)
    # Pull just the symbols for users who received texts this week
    texts_this_week_symbols_only_arr = select_users_received_text_this_week_symbols_only_function(connection_postgres, cursor)

    # Close connection
    close_connection_cursor_to_database_function(connection_postgres, cursor)

    # Tuen the symbols only array into dictionary with weekly thresholds per symbol
    texts_this_week_symbols_only_dict = convert_arr_dict_symbols_this_week_with_change_function(texts_this_week_symbols_only_arr)

    # Turn the user data into a nested dict that included weekly thresholds per symbol
    texts_this_week_dict = convert_arr_dict_texts_this_week_function(texts_this_week_arr, texts_this_week_symbols_only_dict)

    # Loop through nested dictionary and email each person the highlights for the week
    master_string = ''
    for k, v in texts_this_week_dict.items():
      for symbol, v2 in v['symbols'].items():
        string = symbol + ", " + v2['total_percent_change_this_week'] + ", " + v2['google_news_link'] + " \n\n\n"
        master_string += string

      send_email_weekly_recap_sym_thresholds_function(k, v, master_string)
  

# Run the main program
if __name__ == "__main__":
  print('= = = = = = = = = = = = = = = = = JOB START (job_end_of_week_email_recap_function) = = = = = = = = = = = = = = = = =')
  job_end_of_week_email_recap_function()
  print('= = = = = = = = = = = = = = = = = JOB END (job_end_of_week_email_recap_function) = = = = = = = = = = = = = = = = =')