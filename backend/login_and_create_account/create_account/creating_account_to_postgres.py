from flask import Flask, redirect, url_for, request, session, Blueprint
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
from backend.user_logged_in.confirm.confirm_phone_number_page import confirm_phone_number_page
from backend.user_logged_in.confirm.confirm_phone_number_page import confirm_phone_number_page_function
from backend.utils.constant_run.twilio.send_phone_number_confirm_account import send_phone_number_confirm_account_function
from backend.utils.app_before_setup.check_if_url_www import check_if_url_www_function
from backend.utils.app_before_setup.remove_www_from_domain import remove_www_from_domain_function

creating_account_to_postgres = Blueprint("creating_account_to_postgres", __name__, static_folder="static", template_folder="templates")

@creating_account_to_postgres.before_request
def before_request():
  """Returns: The domain should work with both www and non-www domain"""
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=301)

@creating_account_to_postgres.route("/home/created", methods=["POST", "GET"])
def creating_account_to_postgres_function():
  """Returns: Uploads new account info to Postgres database, if it does not already exist."""
  # Check if user session data is already present/signed in
  if session and session.get('logged_in_user_email') != 'none':
    return redirect('https://symbolnews.com/dashboard', code=301)

  try:
    # Get and sanitize the user inputs from html form
    user_first_name_from_html_form_sanitized = sanitize_name_input_create_account_function(request.form.get('user_first_name'))
    user_last_name_from_html_form_sanitized = sanitize_name_input_create_account_function(request.form.get('user_last_name'))
    user_phone_number_from_html_form_sanitized= sanitize_phone_number_input_create_account_function(request.form.get('phone_number'))
    user_email_from_html_form_sanitized = sanitize_email_input_create_account_function(request.form.get('email'))
    user_password_from_html_form_sanitized = sanitize_password_input_create_account_function(request.form.get('psw'))
  except:
    # If user inputs wrong format
    session['create_account_failed_message'] = 'Incorrect format!'
    return redirect("https://symbolnews.com/create_account", code=301)

  # If postman invalid inputs used
  if user_first_name_from_html_form_sanitized == 'none' or user_last_name_from_html_form_sanitized == 'none' or user_phone_number_from_html_form_sanitized == 'none' or user_email_from_html_form_sanitized == 'none' or user_password_from_html_form_sanitized == 'none':
    print('FAILED TO CREATE ACCOUNT!')
    return 'FAILED TO CREATE ACCOUNT!'
  
  # Hash the user password from html form
  hashed_user_password_from_html_form = bcrypt.hashpw(user_password_from_html_form_sanitized.encode('utf-8'), bcrypt.gensalt())
  hashed_user_password_from_html_form_decoded_for_database_insert = hashed_user_password_from_html_form.decode('ascii')
  
  # Connect to postgres
  connection_postgres, cursor = connect_to_postgres_function()
  
  # Search query if email is already in database
  email_exists = select_login_information_table_query_function(connection_postgres, cursor, user_email_from_html_form_sanitized)
  
  # If email account already exists in database 
  if email_exists == 'Account already exists':
    close_connection_cursor_to_database_function(connection_postgres, cursor)
    session['create_account_failed_message'] = 'Account already exists'
    return redirect("https://symbolnews.com/create_account", code=301)
  
  # Add the UUID and timestamp for datetime that the account was created
  user_uuid_create_account = create_uuid_function("user_")
  user_create_account_timestamp = create_timestamp_function()

  # Insert query function to insert new user created data into postgres
  success_message, error_message = insert_login_information_table_query_function(connection_postgres, cursor, user_uuid_create_account, user_create_account_timestamp, user_first_name_from_html_form_sanitized, user_last_name_from_html_form_sanitized, user_phone_number_from_html_form_sanitized, user_email_from_html_form_sanitized, hashed_user_password_from_html_form_decoded_for_database_insert)
  
  # Close database connection and cursor
  close_connection_cursor_to_database_function(connection_postgres, cursor)
  
  # Continue based on query insert results
  if success_message == 'success' and error_message == 'none':
    # Create tokens for email and phone number verification
    confirm_email_token = create_confirm_token_function(user_email_from_html_form_sanitized, os.environ.get('URL_SAFE_SERIALIZER_SECRET_KEY_EMAIL'), os.environ.get('URL_SAFE_SERIALIZER_SECRET_SALT_EMAIL'))
    confirm_phone_number_token = create_confirm_token_function(user_phone_number_from_html_form_sanitized, os.environ.get('URL_SAFE_SERIALIZER_SECRET_KEY_PHONE'), os.environ.get('URL_SAFE_SERIALIZER_SECRET_SALT_PHONE'))
    
    # Create the URL links for email and phone number verification
    url_for('confirm_email_page.confirm_email_page_function', confirm_email_token_url_variable = confirm_email_token)
    url_for('confirm_phone_number_page.confirm_phone_number_page_function', confirm_phone_number_token_url_variable = confirm_phone_number_token)
    
    # Send the confirmation email and text links to user
    send_email_confirm_account_function(user_email_from_html_form_sanitized, user_first_name_from_html_form_sanitized, confirm_email_token)
    send_phone_number_confirm_account_function(user_phone_number_from_html_form_sanitized, user_first_name_from_html_form_sanitized, confirm_phone_number_token)
    
    # Flask set session variables and redirect to dashboard
    session['logged_in_user_uuid'] = user_uuid_create_account
    session['logged_in_user_email'] = user_email_from_html_form_sanitized
    session['logged_in_user_first_name'] = user_first_name_from_html_form_sanitized
    session['logged_in_user_last_name'] = user_last_name_from_html_form_sanitized
    session['logged_in_user_phone_number'] = user_phone_number_from_html_form_sanitized
    session.permanent = True
    return redirect("https://symbolnews.com/dashboard", code=301)
  
  # If above fails at any point redirect back to create account page
  else:
    set_session_variables_to_none_logout_function()
    return redirect("https://symbolnews.com/create_account", code=301)
  return redirect("https://symbolnews.com/create_account", code=301)