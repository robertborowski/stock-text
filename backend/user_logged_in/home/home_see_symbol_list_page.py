from flask import render_template, Blueprint, session
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.queries.select_queries.select_user_tracking_list import select_user_tracking_list_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function

home_see_symbol_list_page = Blueprint("home_see_symbol_list_page", __name__, static_folder="static", template_folder="templates")
@home_see_symbol_list_page.route("/home/list", methods=["POST", "GET"])
def home_see_symbol_list_page_function():
  """
  Returns: home see symbol list page
  """
  if session['logged_in_user_email'] != 'none':
    connection_postgres, cursor = connect_to_postgres_function()
    symbol_tracking_list = select_user_tracking_list_function(connection_postgres, cursor, session['logged_in_user_uuid'])
    close_connection_cursor_to_database_function(connection_postgres, cursor)
    return render_template('templates_user_logged_in/loggedin_symbol_tracker_list.html', symbol_tracking_list_from_python_to_html = symbol_tracking_list)
  else:
    set_session_variables_to_none_logout_function()
    return render_template('templates_login_and_create_account/index.html')