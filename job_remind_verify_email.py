from flask import Flask, redirect, url_for, request, session, Blueprint
import datetime
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.db.queries.select_queries.select_user_email_not_confirmed_status import select_user_email_not_confirmed_status_function
from backend.login_and_create_account.create_confirm_token import create_confirm_token_function
import os
from backend.user_logged_in.confirm.confirm_email_page import confirm_email_page
from backend.user_logged_in.confirm.confirm_email_page import confirm_email_page_function
from backend.utils.constant_run.twilio.send_reminder_email_confirm_account import send_reminder_email_confirm_account_function

def job_remind_verify_email_function():
  """Return: Should run in the background automatically at intervals"""
  # First check the day
  num_day_of_week = datetime.datetime.today().weekday()
  print(num_day_of_week)
  """if num_day_of_week == 0 or num_day_of_week == 1 or num_day_of_week == 2 or num_day_of_week == 3 or num_day_of_week == 4 or num_day_of_week == 5:
    return True"""
  
  # Connect to database
  connection_postgres, cursor = connect_to_postgres_function()
  # Pull data - all email needed data
  users_not_confirmed_arr = select_user_email_not_confirmed_status_function(connection_postgres, cursor)
  # Close connection
  close_connection_cursor_to_database_function(connection_postgres, cursor)

  if len(users_not_confirmed_arr) > 0:
    for i in users_not_confirmed_arr:
      try:
        if i[0] == 'a@a.com':
          # Create token for verification
          confirm_email_token = create_confirm_token_function(i[0], os.environ.get('URL_SAFE_SERIALIZER_SECRET_KEY_EMAIL'), os.environ.get('URL_SAFE_SERIALIZER_SECRET_SALT_EMAIL'))
          # Create the URL link for verification
          try:
            url_for('confirm_email_page.confirm_email_page_function', confirm_email_token_url_variable = confirm_email_token)
          except:
            pass
          # Message the confirmation link to user
          send_reminder_email_confirm_account_function(i[0], i[1], confirm_email_token)
      except:
        pass


# Run the main program
if __name__ == "__main__":
  job_remind_verify_email_function()