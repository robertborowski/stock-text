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
from backend.utils.create_uuid import create_uuid_function
from backend.utils.create_timestamp import create_timestamp_function
from backend.db.queries.insert_queries.insert_reminder_email_table import insert_reminder_email_table_function

def job_remind_verify_email_function():
  """Return: Send reminder email to users to verify their email"""
  # First check the day
  num_day_of_week = datetime.datetime.today().weekday()
  if num_day_of_week == 0 or num_day_of_week == 1 or num_day_of_week == 2 or num_day_of_week == 3 or num_day_of_week == 4 or num_day_of_week == 5:
    return True
  
  # Connect to database
  connection_postgres, cursor = connect_to_postgres_function()
  # Pull data - all email needed data
  users_not_confirmed_arr = select_user_email_not_confirmed_status_function(connection_postgres, cursor)
  
  if len(users_not_confirmed_arr) > 0:
    for i in users_not_confirmed_arr:
      try:
        # Create token for verification
        confirm_email_token = create_confirm_token_function(i[0], os.environ.get('URL_SAFE_SERIALIZER_SECRET_KEY_EMAIL'), os.environ.get('URL_SAFE_SERIALIZER_SECRET_SALT_EMAIL'))
        # Create the URL link for verification
        try:
          url_for('confirm_email_page.confirm_email_page_function', confirm_email_token_url_variable = confirm_email_token)
        except:
          pass
        # Message the confirmation link to user
        send_reminder_email_confirm_account_function(i[0], i[1], confirm_email_token)

        # Add the UUID and timestamp for datetime that the reminder was created/sent
        uuid_reminder_email = create_uuid_function("rmde_")
        reminder_email_timestamp = create_timestamp_function()

        # Insert data into database table
        attempt_insert_reminder_email = insert_reminder_email_table_function(connection_postgres, cursor, uuid_reminder_email, reminder_email_timestamp, i[2], confirm_email_token)
        print(attempt_insert_reminder_email)
      except:
        pass
  # Close connection
  close_connection_cursor_to_database_function(connection_postgres, cursor)

# Run the main program
if __name__ == "__main__":
  print('= = = = = = = = = = = = = = = = = JOB START (job_remind_verify_email_function) = = = = = = = = = = = = = = = = =')
  job_remind_verify_email_function()
  print('= = = = = = = = = = = = = = = = = JOB END (job_remind_verify_email_function) = = = = = = = = = = = = = = = = =')