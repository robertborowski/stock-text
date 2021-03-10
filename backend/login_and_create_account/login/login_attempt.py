from flask import Flask, redirect, request, session, Blueprint
import bcrypt
import psycopg2
from psycopg2 import Error
from backend.utils.sanitize_user_inputs.sanitize_email_input_create_account import sanitize_email_input_create_account_function
from backend.utils.sanitize_user_inputs.sanitize_password_input_create_account import sanitize_password_input_create_account_function
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.queries.select_queries.select_password_query import select_password_query_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function

login_attempt = Blueprint("login_attempt", __name__, static_folder="static", template_folder="templates")
@login_attempt.route("/login_attempt", methods=["POST", "GET"])
def login_attempt_function():
  """Returns: login attempt on the login_page"""
  # Check if user session data is already present/signed in
  if session and session.get('logged_in_user_email') != 'none':
    return redirect('https://symbolnews.com/dashboard', code=301)
  
  # Sanitize user inputs
  user_email_from_html_form_sanitized = sanitize_email_input_create_account_function(request.form.get('email'))
  user_password_from_html_form_sanitized = sanitize_password_input_create_account_function(request.form.get('psw'))
  
  # If postman invalid inputs used
  if user_email_from_html_form_sanitized == 'none' or user_password_from_html_form_sanitized == 'none':
    print('FAILED TO LOGIN!')
    return 'FAILED TO LOGIN!'

  # Login attempt with valid inputs
  connection_postgres, cursor = connect_to_postgres_function()
  session['logged_in_user_uuid'], session['logged_in_user_email'], session['logged_in_user_first_name'], session['logged_in_user_last_name'], session['logged_in_user_phone_number'] = select_password_query_function(connection_postgres, cursor, user_email_from_html_form_sanitized, user_password_from_html_form_sanitized)
  close_connection_cursor_to_database_function(connection_postgres, cursor)
  
  # Login attempt fail
  if session['logged_in_user_email'] == 'none' or session['logged_in_user_first_name'] == 'none' or session['logged_in_user_last_name'] == 'none' or session['logged_in_user_phone_number'] == 'none':
    session['login_failed_message'] = 'Email/Password not found!'
    return redirect("https://symbolnews.com/", code=301)
  
  # Login attempt Success
  else:
    session.permanent = True
    return redirect("/dashboard", code=301)
    #return redirect("https://symbolnews.com/dashboard", code=301)