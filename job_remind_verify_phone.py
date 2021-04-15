from flask import Flask, redirect, url_for, request, session, Blueprint
import datetime
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.db.queries.select_queries.select_user_phone_not_confirmed_status import select_user_phone_not_confirmed_status_function
from backend.login_and_create_account.create_confirm_token import create_confirm_token_function
import os
from backend.user_logged_in.confirm.confirm_phone_number_page import confirm_phone_number_page
from backend.user_logged_in.confirm.confirm_phone_number_page import confirm_phone_number_page_function
from backend.utils.constant_run.twilio.send_reminder_phone_confirm_account import send_reminder_phone_confirm_account_function
from backend.utils.create_uuid import create_uuid_function
from backend.utils.create_timestamp import create_timestamp_function
from backend.db.queries.insert_queries.insert_reminder_phone_table import insert_reminder_phone_table_function

def job_remind_verify_phone_function():
  """Return: Send reminder text to users to verify their phone number"""
  # First check the day
  num_day_of_week = datetime.datetime.today().weekday()
  if num_day_of_week == 0 or num_day_of_week == 1 or num_day_of_week == 2 or num_day_of_week == 3 or num_day_of_week == 4 or num_day_of_week == 5:
    return True
  
  # Connect to database
  connection_postgres, cursor = connect_to_postgres_function()
  # Pull data - all phone needed data
  users_not_confirmed_arr = select_user_phone_not_confirmed_status_function(connection_postgres, cursor)
  
  if len(users_not_confirmed_arr) > 0:
    for i in users_not_confirmed_arr:
      try:
        # Create token for verification
        confirm_phone_number_token = create_confirm_token_function(i[0], os.environ.get('URL_SAFE_SERIALIZER_SECRET_KEY_PHONE'), os.environ.get('URL_SAFE_SERIALIZER_SECRET_SALT_PHONE'))
        # Create the URL link for verification
        try:
          url_for('confirm_phone_number_page.confirm_phone_number_page_function', confirm_phone_number_token_url_variable = confirm_phone_number_token)
        except:
          pass
        # Message the confirmation link to user
        twilio_message_sid = send_reminder_phone_confirm_account_function(i[0], i[1], confirm_phone_number_token)

        # Add the UUID and timestamp for datetime that the reminder was created/sent
        uuid_reminder_phone = create_uuid_function("rmdp_")
        reminder_phone_timestamp = create_timestamp_function()

        # Insert data into database table
        attempt_insert_reminder_phone = insert_reminder_phone_table_function(connection_postgres, cursor, uuid_reminder_phone, reminder_phone_timestamp, i[2], confirm_phone_number_token, twilio_message_sid)
        print(attempt_insert_reminder_phone)
      except:
        pass
  # Close connection
  close_connection_cursor_to_database_function(connection_postgres, cursor)

# Run the main program
if __name__ == "__main__":
  job_remind_verify_phone_function()