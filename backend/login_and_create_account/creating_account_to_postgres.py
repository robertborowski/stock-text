from flask import Flask, redirect, url_for, render_template, request, session, Blueprint
import os
import bcrypt
from backend.utils.sanitize_user_inputs.sanitize_name_input_create_account import sanitize_name_input_create_account_function
from backend.utils.sanitize_user_inputs.sanitize_phone_number_input_create_account import sanitize_phone_number_input_create_account_function
from backend.utils.sanitize_user_inputs.sanitize_email_input_create_account import sanitize_email_input_create_account_function
from backend.utils.sanitize_user_inputs.sanitize_password_input_create_account import sanitize_password_input_create_account_function
from backend.utils.create_uuid import create_uuid_function
from backend.utils.create_timestamp import create_timestamp_function
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.queries.insert_queries.insert_login_information_table_query import insert_login_information_table_query_function
from backend.db.queries.select_queries.select_login_information_table_query import select_login_information_table_query_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function
from backend.utils.constant_run.twilio.send_email_confirm_account import send_email_confirm_account_function
from backend.login_and_create_account.create_confirm_token import create_confirm_token_function
from backend.user_logged_in.confirm.confirm_email_page import confirm_email_page
from backend.user_logged_in.confirm.confirm_email_page import confirm_email_page_function

creating_account_to_postgres = Blueprint("creating_account_to_postgres", __name__, static_folder="static", template_folder="templates")
@creating_account_to_postgres.route("/home/created", methods=["POST", "GET"])
def creating_account_to_postgres_function():
  """
  Returns: Uploads new account info to Postgres database, if it does not already exist.
  """
  # Get and sanitize the user inputs from html form
  user_first_name_from_html_form_sanitized = sanitize_name_input_create_account_function(request.form.get("user_first_name"))
  user_last_name_from_html_form_sanitized = sanitize_name_input_create_account_function(request.form.get("user_last_name"))
  user_phone_number_from_html_form_sanitized= sanitize_phone_number_input_create_account_function(request.form.get("phone_number"))
  user_email_from_html_form_sanitized = sanitize_email_input_create_account_function(request.form.get("email"))
  user_password_from_html_form_sanitized = sanitize_password_input_create_account_function(request.form.get('psw'))
  # If none for all input variables
  if user_first_name_from_html_form_sanitized == 'none' or user_last_name_from_html_form_sanitized == 'none' or user_phone_number_from_html_form_sanitized == 'none' or user_email_from_html_form_sanitized == 'none' or user_password_from_html_form_sanitized == 'none':
    print('FAILED TO CREATE ACCOUNT!')
    return 'FAILED TO CREATE ACCOUNT!'
  # Hash the user password from html form
  hashed_user_password_from_html_form = bcrypt.hashpw(user_password_from_html_form_sanitized.encode('utf-8'), bcrypt.gensalt())
  hashed_user_password_from_html_form_decoded_for_database_insert = hashed_user_password_from_html_form.decode('ascii')
  # Add the UUID and timestamp for datetime that the account was created
  user_uuid_create_account = create_uuid_function("usr_")
  user_create_account_timestamp = create_timestamp_function()
  # Connect to postgres
  connection_postgres, cursor = connect_to_postgres_function()
  # Search query if email is already in database
  email_exists = select_login_information_table_query_function(connection_postgres, cursor, user_email_from_html_form_sanitized)
  if email_exists == 'Account already exists':
    close_connection_cursor_to_database_function(connection_postgres, cursor)
    return render_template('templates_login_and_create_account/create_account.html', error_message_from_python_to_html = email_exists)
  # Insert query function to postgres
  success_message, error_message = insert_login_information_table_query_function(connection_postgres, cursor, user_uuid_create_account, user_create_account_timestamp, user_first_name_from_html_form_sanitized, user_last_name_from_html_form_sanitized, user_phone_number_from_html_form_sanitized, user_email_from_html_form_sanitized, hashed_user_password_from_html_form_decoded_for_database_insert)
  # Close database connection and cursor
  close_connection_cursor_to_database_function(connection_postgres, cursor)
  # Continue based on query insert results
  if success_message == 'success' and error_message == 'none':
    # Create tokens for email and phone number verification
    confirm_email_token = create_confirm_token_function(user_email_from_html_form_sanitized, os.environ.get('URL_SAFE_SERIALIZER_SECRET_KEY_EMAIL'), os.environ.get('URL_SAFE_SERIALIZER_SECRET_SALT_EMAIL'))
    #confirm_phone_number_token = create_confirm_token_function(user_phone_number_from_html_form_sanitized)
    # Create the URL links for email and phone number verification
    url_for('confirm_email_page.confirm_email_page_function', confirm_email_token_url_variable = confirm_email_token)
    send_email_confirm_account_function(user_email_from_html_form_sanitized, user_first_name_from_html_form_sanitized, confirm_email_token)
    output_message = 'Please confirm email (link sent to email) and phone number (link sent to phone number)'
    # Flask session variables
    session['logged_in_user_uuid'] = user_uuid_create_account
    session['logged_in_user_email'] = user_email_from_html_form_sanitized
    session['logged_in_user_first_name'] = user_first_name_from_html_form_sanitized
    session['logged_in_user_last_name'] = user_last_name_from_html_form_sanitized
    session['logged_in_user_phone_number'] = user_phone_number_from_html_form_sanitized
    return render_template('templates_user_logged_in/loggedin_home_page.html',
                            user_email_from_session_to_html = session['logged_in_user_email'],
                            user_first_name_from_session_to_html = session['logged_in_user_first_name'],
                            user_last_name_from_session_to_html = session['logged_in_user_last_name'],
                            user_phone_number_from_session_to_html = session['logged_in_user_phone_number'],
                            output_message_to_html = output_message)
  else:
    set_session_variables_to_none_logout_function()
    return render_template('templates_login_and_create_account/create_account.html', error_message_from_python_to_html = error_message)
  return render_template('templates_login_and_create_account/create_account.html', error_message_from_python_to_html = error_message)