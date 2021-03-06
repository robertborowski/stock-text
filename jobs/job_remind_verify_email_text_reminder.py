from flask import Flask, redirect, url_for, request, session, Blueprint
import datetime
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.db.queries.select_queries.select_user_email_not_confirmed_status_but_phone_yes_confirmed import select_user_email_not_confirmed_status_but_phone_yes_confirmed_function
from backend.login_and_create_account.create_confirm_token import create_confirm_token_function
import os
from backend.user_logged_in.confirm.confirm_phone_number_page import confirm_phone_number_page
from backend.user_logged_in.confirm.confirm_phone_number_page import confirm_phone_number_page_function
from backend.utils.constant_run.twilio.send_reminder_phone_to_confirm_email_account import send_reminder_phone_to_confirm_email_account_function
from backend.utils.create_uuid import create_uuid_function
from backend.utils.create_timestamp import create_timestamp_function
from backend.db.queries.insert_queries.insert_reminder_phone_table import insert_reminder_phone_table_function

def job_remind_verify_email_text_reminder_function():
  """Return: Send reminder text to users to verify their emails/check spam folder"""
  # First check the day
  num_day_of_week = datetime.datetime.today().weekday()
  if num_day_of_week == 0 or num_day_of_week == 1 or num_day_of_week == 2 or num_day_of_week == 3 or num_day_of_week == 4 or num_day_of_week == 5:
    return True
  
  # Connect to database
  connection_postgres, cursor = connect_to_postgres_function()
  # Pull data - all phone needed data
  users_not_confirmed_arr = select_user_email_not_confirmed_status_but_phone_yes_confirmed_function(connection_postgres, cursor)
  
  if len(users_not_confirmed_arr) > 0:
    for i in users_not_confirmed_arr:
      try:
        # Message the confirmation link to user
        twilio_message_sid = send_reminder_phone_to_confirm_email_account_function(i[0], i[1], i[2])

        # Add the UUID and timestamp for datetime that the reminder was created/sent
        uuid_reminder_phone = create_uuid_function("rdpe_")
        reminder_phone_timestamp = create_timestamp_function()
        confirm_phone_number_token = ''

        # Insert data into database table
        attempt_insert_reminder_phone = insert_reminder_phone_table_function(connection_postgres, cursor, uuid_reminder_phone, reminder_phone_timestamp, i[3], confirm_phone_number_token, twilio_message_sid)
        print(attempt_insert_reminder_phone)
      except:
        pass
  # Close connection
  close_connection_cursor_to_database_function(connection_postgres, cursor)

# Run the main program
if __name__ == "__main__":
  print('= = = = = = = = = = = = = = = = = JOB START (job_remind_verify_email_text_reminder_function) = = = = = = = = = = = = = = = = =')
  job_remind_verify_email_text_reminder_function()
  print('= = = = = = = = = = = = = = = = = JOB END (job_remind_verify_email_text_reminder_function) = = = = = = = = = = = = = = = = =')