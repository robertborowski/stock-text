from flask import render_template, Blueprint, session, redirect, request
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.db.queries.delete_queries.delete_all_user_symbol_tracking_table_data import delete_all_user_symbol_tracking_table_data_function
from backend.db.queries.delete_queries.delete_all_user_login_information_table_data import delete_all_user_login_information_table_data_function
from backend.utils.app_before_setup.check_if_url_www import check_if_url_www_function
from backend.utils.app_before_setup.remove_www_from_domain import remove_www_from_domain_function

delete_account_perm = Blueprint("delete_account_perm", __name__, static_folder="static", template_folder="templates")

@delete_account_perm.before_request
def before_request():
  """Returns: The domain should work with both www and non-www domain"""
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=301)

@delete_account_perm.route("/account/delete/confirm", methods=["POST", "GET"])
def delete_account_perm_function():
  if session['logged_in_user_email'] != 'none':
    connection_postgres, cursor = connect_to_postgres_function()
    delete_all_user_symbol_tracking_table_data_function(connection_postgres, cursor, session['logged_in_user_uuid'])
    delete_all_user_login_information_table_data_function(connection_postgres, cursor, session['logged_in_user_uuid'])
    close_connection_cursor_to_database_function(connection_postgres, cursor)
    set_session_variables_to_none_logout_function()
    session['login_failed_message'] = 'Account deleted!'
    return redirect("https://symbolnews.com/", code=301)
  else:
    set_session_variables_to_none_logout_function()
    return redirect("https://symbolnews.com/", code=301)