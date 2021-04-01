from flask import render_template, Blueprint, session, redirect, request, url_for
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function
from backend.utils.sanitize_user_inputs.sanitize_email_input_create_account import sanitize_email_input_create_account_function
from backend.utils.sanitize_user_inputs.sanitize_name_input_create_account import sanitize_name_input_create_account_function
from backend.utils.sanitize_user_inputs.sanitize_phone_number_input_create_account import sanitize_phone_number_input_create_account_function
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.db.queries.update_queries.update_user_info import update_user_info_function
from backend.db.queries.update_queries.update_user_email_verified_false import update_user_email_verified_false_function
from backend.db.queries.update_queries.update_user_phone_verified_false import update_user_phone_verified_false_function
from backend.utils.app_before_setup.check_if_url_www import check_if_url_www_function
from backend.utils.app_before_setup.remove_www_from_domain import remove_www_from_domain_function
from backend.db.queries.select_queries.select_login_information_table_query import select_login_information_table_query_function
from backend.db.queries.select_queries.select_login_information_table_query_phone_number import select_login_information_table_query_phone_number_function
from backend.login_and_create_account.create_confirm_token import create_confirm_token_function
import os
from backend.user_logged_in.confirm.confirm_email_page import confirm_email_page
from backend.user_logged_in.confirm.confirm_email_page import confirm_email_page_function
from backend.user_logged_in.confirm.confirm_phone_number_page import confirm_phone_number_page
from backend.user_logged_in.confirm.confirm_phone_number_page import confirm_phone_number_page_function
from backend.utils.constant_run.twilio.send_email_confirm_account import send_email_confirm_account_function
from backend.utils.constant_run.twilio.send_phone_number_confirm_account import send_phone_number_confirm_account_function
from backend.db.queries.update_queries.update_user_first_name import update_user_first_name_function
from backend.db.queries.update_queries.update_user_last_name import update_user_last_name_function
from backend.db.queries.update_queries.update_user_email import update_user_email_function
from backend.db.queries.update_queries.update_user_phone import update_user_phone_function

updating_account_info_postgres = Blueprint("updating_account_info_postgres", __name__, static_folder="static", template_folder="templates")

@updating_account_info_postgres.before_request
def before_request():
  """Returns: The domain should work with both www and non-www domain"""
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=301)

@updating_account_info_postgres.route("/account/edit/upload", methods=["POST", "GET"])
def updating_account_info_postgres_function():
  # If no account information was updated
  if request.form.get("email") == session['logged_in_user_email'] and request.form.get("user_first_name") == session['logged_in_user_first_name'] and request.form.get("user_last_name") == session['logged_in_user_last_name'] and request.form.get("phone_number") == session['logged_in_user_phone_number']:
    return redirect("https://symbolnews.com/account", code=301)

  # Check if email was updated, then sanitize input
  if request.form.get("email") != session['logged_in_user_email']:
    user_email_from_html_form_sanitized = sanitize_email_input_create_account_function(request.form.get("email"))
  else:
    user_email_from_html_form_sanitized = session['logged_in_user_email']

  # Check if first name was updated, then sanitize input
  if request.form.get("user_first_name") != session['logged_in_user_first_name']:
    user_first_name_from_html_form_sanitized = sanitize_name_input_create_account_function(request.form.get("user_first_name"))
  else:
    user_first_name_from_html_form_sanitized = session['logged_in_user_first_name']
  
  # Check if last name was updated, then sanitize input
  if request.form.get("user_last_name") != session['logged_in_user_last_name']:
    user_last_name_from_html_form_sanitized = sanitize_name_input_create_account_function(request.form.get("user_last_name"))
  else:
    user_last_name_from_html_form_sanitized = session['logged_in_user_last_name']
  
  # Check if phone number was updated, then sanitize input
  if request.form.get("phone_number") != session['logged_in_user_phone_number']:
    user_phone_number_from_html_form_sanitized = sanitize_phone_number_input_create_account_function(request.form.get("phone_number"))
  else:
    user_phone_number_from_html_form_sanitized = session['logged_in_user_phone_number']

  # If any invalid inputs/changes for form
  if user_email_from_html_form_sanitized == 'none' or user_first_name_from_html_form_sanitized == 'none' or user_last_name_from_html_form_sanitized == 'none' or user_phone_number_from_html_form_sanitized == 'none':
    print('FAILED TO CREATE ACCOUNT!')
    return 'FAILED TO UPDATE ACCOUNT!'

  # If valid inputs/changes for form
  if session['logged_in_user_email'] != 'none':
    # Connect to Database
    connection_postgres, cursor = connect_to_postgres_function()
    
    # Check/Update user first name
    if session['logged_in_user_first_name'] != user_first_name_from_html_form_sanitized:
      update_user_first_name_function(connection_postgres, cursor, user_first_name_from_html_form_sanitized, session['logged_in_user_uuid'])
      session['logged_in_user_first_name'] = user_first_name_from_html_form_sanitized

    # Check/Update user last name
    if session['logged_in_user_last_name'] != user_last_name_from_html_form_sanitized:
      update_user_last_name_function(connection_postgres, cursor, user_last_name_from_html_form_sanitized, session['logged_in_user_uuid'])
      session['logged_in_user_last_name'] = user_last_name_from_html_form_sanitized

    # Check/Update email
    if session['logged_in_user_email'] != user_email_from_html_form_sanitized:
      does_email_exist = select_login_information_table_query_function(connection_postgres, cursor, user_email_from_html_form_sanitized)
      if does_email_exist == 'Account already exists':
        output_message = 'Cannot use that email/phone number combination'
        return redirect("https://symbolnews.com/account", code=301)
      else:
        update_user_email_function(connection_postgres, cursor, user_email_from_html_form_sanitized, session['logged_in_user_uuid'])
        session['logged_in_user_email'] = user_email_from_html_form_sanitized
        update_user_email_verified_false_function(connection_postgres, cursor, session['logged_in_user_uuid'])
        confirm_email_token = create_confirm_token_function(user_email_from_html_form_sanitized, os.environ.get('URL_SAFE_SERIALIZER_SECRET_KEY_EMAIL'), os.environ.get('URL_SAFE_SERIALIZER_SECRET_SALT_EMAIL'))
        url_for('confirm_email_page.confirm_email_page_function', confirm_email_token_url_variable = confirm_email_token)
        send_email_confirm_account_function(user_email_from_html_form_sanitized, user_first_name_from_html_form_sanitized, confirm_email_token)

    # Check/Update phone number
    if session['logged_in_user_phone_number'] != user_phone_number_from_html_form_sanitized:
      does_phone_number_exist = select_login_information_table_query_phone_number_function(connection_postgres, cursor, user_phone_number_from_html_form_sanitized)
      if does_phone_number_exist == 'Account already exists':
        output_message = 'Cannot use that email/phone number combination'
        return redirect("https://symbolnews.com/account", code=301)
      else:
        update_user_phone_function(connection_postgres, cursor, user_phone_number_from_html_form_sanitized, session['logged_in_user_uuid'])
        session['logged_in_user_phone_number'] = user_phone_number_from_html_form_sanitized
        update_user_phone_verified_false_function(connection_postgres, cursor, session['logged_in_user_uuid'])
        confirm_phone_number_token = create_confirm_token_function(user_phone_number_from_html_form_sanitized, os.environ.get('URL_SAFE_SERIALIZER_SECRET_KEY_PHONE'), os.environ.get('URL_SAFE_SERIALIZER_SECRET_SALT_PHONE'))
        url_for('confirm_phone_number_page.confirm_phone_number_page_function', confirm_phone_number_token_url_variable = confirm_phone_number_token)
        send_phone_number_confirm_account_function(user_phone_number_from_html_form_sanitized, user_first_name_from_html_form_sanitized, confirm_phone_number_token)

    # Close connection to database
    close_connection_cursor_to_database_function(connection_postgres, cursor)
    
    output_message = 'Account Changes Saved'
    return redirect("https://symbolnews.com/account", code=301)
  else:
    set_session_variables_to_none_logout_function()
    return redirect("https://symbolnews.com/", code=301)
  