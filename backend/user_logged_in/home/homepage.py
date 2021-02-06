from flask import render_template, Blueprint, session
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.queries.select_queries.select_user_tracking_list import select_user_tracking_list_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function

homepage = Blueprint("homepage", __name__, static_folder="static", template_folder="templates")
@homepage.route("/home", methods=["POST", "GET"])
def logged_in_home_page_function():
  """
  Returns: homepage front end template
  """
  if session['logged_in_user_email'] != 'none':
    connection_postgres, cursor = connect_to_postgres_function()
    symbol_tracking_list = select_user_tracking_list_function(connection_postgres, cursor, session['logged_in_user_uuid'])
    close_connection_cursor_to_database_function(connection_postgres, cursor)
    return render_template('templates_user_logged_in/loggedin_home_page.html',
                            user_email_from_session_to_html = session['logged_in_user_email'],
                            user_first_name_from_session_to_html = session['logged_in_user_first_name'],
                            user_last_name_from_session_to_html = session['logged_in_user_last_name'],
                            user_phone_number_from_session_to_html = session['logged_in_user_phone_number'],
                            symbol_tracking_list_from_python_to_html = symbol_tracking_list)
  else:
    set_session_variables_to_none_logout_function()
    return render_template('templates_login_and_create_account/index.html')