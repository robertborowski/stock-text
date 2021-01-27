from flask import Flask, redirect, url_for, render_template, request, session, Blueprint
import bcrypt
import psycopg2
from psycopg2 import Error
from backend.db.connect_to_database import connect_to_postgres_function
login_attempt = Blueprint("login_attempt", __name__, static_folder="static", template_folder="templates")
@login_attempt.route("/login_attempt", methods=["POST", "GET"])
def login_attempt_function():
  """
  Returns: login attempt on index/login page
  """
  # Get the user inputs from html form
  user_email_from_html_form = request.form.get("email")
  user_password_from_html_form = request.form.get("psw")
  # Connect to postgres
  connection_postgres, cursor = connect_to_postgres_function()
  try:
    # Execute the insert query on database
    cursor.execute("SELECT password, name, phone_number FROM login_information_table WHERE email=%s", [user_email_from_html_form])
    # Get the result from SQL query
    row = cursor.fetchone()
    salted_password = row[0].encode('ascii')
    # Compare the user inut form password with pulled postgres password
    if bcrypt.checkpw(user_password_from_html_form.encode('utf-8'), salted_password):
      # Set the user session info
      session['logged_in_user_email'] = user_email_from_html_form
      session['logged_in_user_name'] = row[1]
      session['logged_in_user_phone_number'] = row[2]
      return render_template('templates_user_logged_in/loggedin_home_page.html',
                              user_email_from_session_to_html = session['logged_in_user_email'],
                              user_name_from_session_to_html = session['logged_in_user_name'],
                              user_phone_number_from_session_to_html = session['logged_in_user_phone_number'])
    else:
      session['logged_in_user_email'] = 'none'
      session['logged_in_user_name'] = 'none'
      session['logged_in_user_phone_number'] = 'none'
      error_message = 'Incorrect Email/Password!'
  except (Exception, psycopg2.Error) as error :
    if(connection_postgres):
      session['logged_in_user_email'] = 'none'
      session['logged_in_user_name'] = 'none'
      session['logged_in_user_phone_number'] = 'none'
      print("ERROR: ", error)
      error_message = 'Incorrect Email/Password!'
      return render_template('templates_login_and_create_account/index.html', error_message_from_python_to_html = error_message)
  finally:
    if(connection_postgres):
      cursor.close()
      connection_postgres.close()
  return render_template('templates_login_and_create_account/index.html', error_message_from_python_to_html = error_message)