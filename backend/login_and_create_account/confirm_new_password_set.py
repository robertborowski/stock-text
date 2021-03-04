from flask import Flask, redirect, url_for, render_template, request, session, Blueprint, current_app
from itsdangerous import URLSafeTimedSerializer
from backend.utils.sanitize_user_inputs.sanitize_password_input_create_account import sanitize_password_input_create_account_function
import os
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
import bcrypt
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.queries.update_queries.update_password import update_password_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.utils.app_before_setup.check_if_url_www import check_if_url_www_function
from backend.utils.app_before_setup.remove_www_from_domain import remove_www_from_domain_function

confirm_new_password_set = Blueprint("confirm_new_password_set", __name__, static_folder="static", template_folder="templates")
@confirm_new_password_set.route("/confirm_new_password_set", methods=["POST", "GET"])
def confirm_new_password_set_function():
  """
  Returns: confirms new password was set
  """
  # Domain Check #1 - Does it start with www.
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    # Redirect page to non-www
    return redirect(new_url, code=301)

  # Sanitize new password
  user_password_from_html_form_sanitized = sanitize_password_input_create_account_function(request.form.get('psw'))
  
  # If none for all input variables
  if user_password_from_html_form_sanitized == 'none':
    print('FAILED TO CREATE ACCOUNT!')
    return 'FAILED TO CREATE ACCOUNT!'
  
  # Hash the user password from html form
  hashed_user_password_from_html_form = bcrypt.hashpw(user_password_from_html_form_sanitized.encode('utf-8'), bcrypt.gensalt())
  hashed_user_password_from_html_form_decoded_for_database_insert = hashed_user_password_from_html_form.decode('ascii')
  
  # Connect to postgres and update password
  connection_postgres, cursor = connect_to_postgres_function()
  update_password_function(connection_postgres, cursor, hashed_user_password_from_html_form_decoded_for_database_insert, session['user_email_to_change_password'])
  close_connection_cursor_to_database_function(connection_postgres, cursor)
  
  return render_template('templates_login_and_create_account/index.html')