from flask import Flask, redirect, url_for, render_template, request, session, Blueprint
import os
import psycopg2
from psycopg2 import Error
from backend.utils.sanitize_user_inputs.sanitize_email_input_create_account import sanitize_email_input_create_account_function
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.db.queries.select_queries.select_login_information_table_query import select_login_information_table_query_function
from backend.login_and_create_account.create_confirm_token import create_confirm_token_function
from backend.utils.constant_run.twilio.send_email_new_password import send_email_new_password_function
from backend.login_and_create_account.set_new_password import set_new_password
from backend.login_and_create_account.set_new_password import set_new_password_function

forgot_password_send_token_to_email = Blueprint("forgot_password_send_token_to_email", __name__, static_folder="static", template_folder="templates")
@forgot_password_send_token_to_email.route("/forgot_password/send_link_attempt", methods=["POST", "GET"])
def forgot_password_send_token_to_email_function():
  """
  Returns: login attempt on index/login page
  """
  user_email_from_html_form_sanitized = sanitize_email_input_create_account_function(request.form.get("email"))
  if user_email_from_html_form_sanitized == 'none':
    print('FAILED TO LOGIN!')
    return 'FAILED TO LOGIN!'
  # Once logged in
  connection_postgres, cursor = connect_to_postgres_function()
  does_email_exist = select_login_information_table_query_function(connection_postgres, cursor, user_email_from_html_form_sanitized)
  close_connection_cursor_to_database_function(connection_postgres, cursor)
  if does_email_exist == 'Account already exists':
    # Create tokens for email and phone number verification
    confirm_email_token = create_confirm_token_function(user_email_from_html_form_sanitized, os.environ.get('URL_SAFE_SERIALIZER_SECRET_KEY_EMAIL'), os.environ.get('URL_SAFE_SERIALIZER_SECRET_SALT_EMAIL'))
    # Create the URL links for email and phone number verification
    url_for('set_new_password.set_new_password_function', confirm_email_token_url_variable = confirm_email_token)
    # Send the confirmation email and text links to user
    send_email_new_password_function(user_email_from_html_form_sanitized, confirm_email_token)
    return render_template('templates_login_and_create_account/forgot_password_page.html', error_message_from_python_to_html = 'Email sent!')
  else:
    return render_template('templates_login_and_create_account/forgot_password_page.html', error_message_from_python_to_html = 'Incorrect Email')