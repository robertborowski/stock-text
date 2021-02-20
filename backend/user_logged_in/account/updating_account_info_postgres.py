from flask import render_template, Blueprint, session, request
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function
from backend.utils.sanitize_user_inputs.sanitize_email_input_create_account import sanitize_email_input_create_account_function
from backend.utils.sanitize_user_inputs.sanitize_name_input_create_account import sanitize_name_input_create_account_function
from backend.utils.sanitize_user_inputs.sanitize_phone_number_input_create_account import sanitize_phone_number_input_create_account_function
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.db.queries.update_queries.update_user_info import update_user_info_function

updating_account_info_postgres = Blueprint("updating_account_info_postgres", __name__, static_folder="static", template_folder="templates")
@updating_account_info_postgres.route("/account/edit/upload", methods=["POST", "GET"])
def updating_account_info_postgres_function():
  if request.form.get("email") == session['logged_in_user_email'] and request.form.get("user_first_name") == session['logged_in_user_first_name'] and request.form.get("user_last_name") == session['logged_in_user_last_name'] and request.form.get("phone_number") == session['logged_in_user_phone_number']:
    output_message = 'Account Unchanged'
    return render_template('templates_user_logged_in/account.html',
                            user_email_from_session_to_html = session['logged_in_user_email'],
                            user_first_name_from_session_to_html = session['logged_in_user_first_name'],
                            user_last_name_from_session_to_html = session['logged_in_user_last_name'],
                            user_phone_number_from_session_to_html = session['logged_in_user_phone_number'],
                            output_message_to_html = output_message)
                            
  if request.form.get("email") != session['logged_in_user_email']:
    user_email_from_html_form_sanitized = sanitize_email_input_create_account_function(request.form.get("email"))
  else:
    user_email_from_html_form_sanitized = session['logged_in_user_email']
  if request.form.get("user_first_name") != session['logged_in_user_first_name']:
    user_first_name_from_html_form_sanitized = sanitize_name_input_create_account_function(request.form.get("user_first_name"))
  else:
    user_first_name_from_html_form_sanitized = session['logged_in_user_first_name']
  if request.form.get("user_last_name") != session['logged_in_user_last_name']:
    user_last_name_from_html_form_sanitized = sanitize_name_input_create_account_function(request.form.get("user_last_name"))
  else:
    user_last_name_from_html_form_sanitized = session['logged_in_user_last_name']
  if request.form.get("phone_number") != session['logged_in_user_phone_number']:
    user_phone_number_from_html_form_sanitized = sanitize_phone_number_input_create_account_function(request.form.get("phone_number"))
  else:
    user_phone_number_from_html_form_sanitized = session['logged_in_user_phone_number']

  if user_email_from_html_form_sanitized == 'none' or user_first_name_from_html_form_sanitized == 'none' or user_last_name_from_html_form_sanitized == 'none' or user_phone_number_from_html_form_sanitized == 'none':
    print('FAILED TO CREATE ACCOUNT!')
    return 'FAILED TO CREATE ACCOUNT!'
  if session['logged_in_user_email'] != 'none':
    connection_postgres, cursor = connect_to_postgres_function()
    update_user_info_function(connection_postgres, cursor, user_email_from_html_form_sanitized, user_first_name_from_html_form_sanitized, user_last_name_from_html_form_sanitized, user_phone_number_from_html_form_sanitized, session['logged_in_user_uuid'])
    close_connection_cursor_to_database_function(connection_postgres, cursor)
    session['logged_in_user_email'] = user_email_from_html_form_sanitized
    session['logged_in_user_first_name'] = user_first_name_from_html_form_sanitized
    session['logged_in_user_last_name'] = user_last_name_from_html_form_sanitized
    session['logged_in_user_phone_number'] = user_phone_number_from_html_form_sanitized
    output_message = 'Account Changes Saved'
    return render_template('templates_user_logged_in/account.html',
                            user_email_from_session_to_html = session['logged_in_user_email'],
                            user_first_name_from_session_to_html = session['logged_in_user_first_name'],
                            user_last_name_from_session_to_html = session['logged_in_user_last_name'],
                            user_phone_number_from_session_to_html = session['logged_in_user_phone_number'],
                            output_message_to_html = output_message)
  else:
    set_session_variables_to_none_logout_function()
    return render_template('templates_login_and_create_account/index.html')
  