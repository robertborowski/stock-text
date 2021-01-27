from flask import Flask, redirect, url_for, render_template, request, session, Blueprint
import bcrypt
import psycopg2
from psycopg2 import Error
from backend.db.connect_to_database import connect_to_postgres_function
creating_account_to_postgres = Blueprint("creating_account_to_postgres", __name__, static_folder="static", template_folder="templates")
@creating_account_to_postgres.route("/creating_account_to_postgres", methods=["POST", "GET"])
def creating_account_to_postgres_function():
  """
  Returns: Uploads new account email, name, phone number to Postgres database, if it does not already exist.
  """
  # Get the user inputs from html form
  user_name_from_html_form = request.form.get("user_name").lower()
  user_email_from_html_form = request.form.get("email")
  user_phone_number_from_html_form = request.form.get("phone_number")
  # Hash the user password from html form
  hashed_user_password_from_html_form = bcrypt.hashpw(request.form.get('psw').encode('utf-8'), bcrypt.gensalt())
  hashed_user_password_from_html_form_decoded_for_database_insert = hashed_user_password_from_html_form.decode('ascii')
  # Connect to postgres
  connection_postgres, cursor = connect_to_postgres_function()
  # The insert query blueprint
  postgres_insert_created_account_query = """INSERT INTO login_information_table (email, name, phone_number, password) VALUES (%s, %s, %s, %s)"""
  # The query record to insert
  record_to_insert = (user_email_from_html_form, user_name_from_html_form, user_phone_number_from_html_form, hashed_user_password_from_html_form_decoded_for_database_insert)
  try:
    # Execute the insert query on database
    cursor.execute(postgres_insert_created_account_query, record_to_insert)
    connection_postgres.commit()
    # Set the user session info
    session['logged_in_user_email'] = user_email_from_html_form
    session['logged_in_user_name'] = user_name_from_html_form
    session['logged_in_user_phone_number'] = user_phone_number_from_html_form
    return render_template('templates_user_logged_in/loggedin_home_page.html',
                            user_email_from_session_to_html = session['logged_in_user_email'],
                            user_name_from_session_to_html = session['logged_in_user_name'],
                            user_phone_number_from_session_to_html = session['logged_in_user_phone_number'])
  except (Exception, psycopg2.Error) as error :
    if(connection_postgres):
      session['logged_in_user_email'] = 'none'
      session['logged_in_user_name'] = 'none'
      session['logged_in_user_phone_number'] = 'none'
      print("Status: ", error)
      error_message = 'Email: ' + user_email_from_html_form + ' - account already exists.'
      return render_template('templates_login_and_create_account/create_account.html', error_message_from_python_to_html = error_message)
  finally:
    if(connection_postgres):
      cursor.close()
      connection_postgres.close()
  return render_template('templates_login_and_create_account/create_account.html', error_message_from_python_to_html = error_message)