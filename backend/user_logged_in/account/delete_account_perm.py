from flask import render_template, Blueprint, session, request
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.db.queries.delete_queries.delete_all_user_symbol_tracking_table_data import delete_all_user_symbol_tracking_table_data_function
from backend.db.queries.delete_queries.delete_all_user_login_information_table_data import delete_all_user_login_information_table_data_function

delete_account_perm = Blueprint("delete_account_perm", __name__, static_folder="static", template_folder="templates")
@delete_account_perm.route("/account/delete/confirm", methods=["POST", "GET"])
def delete_account_perm_function():
  if session['logged_in_user_email'] != 'none':
    connection_postgres, cursor = connect_to_postgres_function()
    delete_all_user_symbol_tracking_table_data_function(connection_postgres, cursor, session['logged_in_user_uuid'])
    delete_all_user_login_information_table_data_function(connection_postgres, cursor, session['logged_in_user_uuid'])
    close_connection_cursor_to_database_function(connection_postgres, cursor)
    set_session_variables_to_none_logout_function()
    return render_template('templates_login_and_create_account/index.html')
  else:
    set_session_variables_to_none_logout_function()
    return render_template('templates_login_and_create_account/index.html')