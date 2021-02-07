from flask import render_template, Blueprint, session, request, redirect, url_for
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.queries.select_queries.select_user_tracking_list import select_user_tracking_list_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function
from backend.utils.breakup_symbols_dict_from_ajax import breakup_symbols_dict_from_ajax_function
from backend.utils.yfinance.check_if_all_symbols_arr_exist import check_if_all_symbols_arr_exist_function
from backend.db.queries.delete_queries.delete_from_stock_tracking_table import delete_from_stock_tracking_table_function

delete_symbols = Blueprint("delete_symbols", __name__, static_folder="static", template_folder="templates")
@delete_symbols.route("/delete_symbols", methods=["POST", "GET"])
def delete_symbols_function():
  if session['logged_in_user_email'] != 'none':
    if request.method == 'POST':
      # Get the json symbols from ajax and sanitize/check if they exist
      selected_symbols_to_delete_from_ajax = request.get_json()
      if len(selected_symbols_to_delete_from_ajax) == 0:
        set_session_variables_to_none_logout_function()
        return render_template('templates_login_and_create_account/index.html')
      symbols_arr = breakup_symbols_dict_from_ajax_function(selected_symbols_to_delete_from_ajax)
      all_symbols_arr_exist = check_if_all_symbols_arr_exist_function(symbols_arr)
      if all_symbols_arr_exist == 'none':
        print('This symbol does not exist!')
        set_session_variables_to_none_logout_function()
        return render_template('templates_login_and_create_account/index.html')
      connection_postgres, cursor = connect_to_postgres_function()
      delete_from_stock_tracking_table_function(connection_postgres, cursor, session['logged_in_user_uuid'], symbols_arr)
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