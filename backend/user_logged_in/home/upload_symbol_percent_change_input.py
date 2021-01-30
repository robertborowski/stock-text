from flask import render_template, Blueprint, session, request
from backend.utils.sanitize_user_inputs.sanitize_symbol_input import sanitize_symbol_input_function
from backend.utils.sanitize_user_inputs.sanitize_symbol_percent_change_input import sanitize_symbol_percent_change_input_function
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.queries.insert_queries.insert_stock_tracking_table import insert_stock_tracking_table_function
from backend.utils.create_uuid import create_uuid_function
from backend.utils.create_timestamp import create_timestamp_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.db.queries.select_queries.select_stock_tracking_table_duplicates import select_stock_tracking_table_duplicates_function
upload_symbol_percent_change_input = Blueprint("upload_symbol_percent_change_input", __name__, static_folder="static", template_folder="templates")
@upload_symbol_percent_change_input.route("/upload_symbol_percent_change_input", methods=["POST", "GET"])
def upload_symbol_percent_change_input_function():
  """
  Returns: sanatizes the user input, then uploads it into the database
  """
  # Sanitize/confirm user inputs
  user_symbol_from_html_form_sanitized = sanitize_symbol_input_function(request.form.get('track_symbol'))
  user_symbol_percent_change_from_html_form_sanitized = sanitize_symbol_percent_change_input_function(request.form.get('track_percent_change'))
  if user_symbol_from_html_form_sanitized == 'none' or user_symbol_percent_change_from_html_form_sanitized == 'none':
    output_message = 'Stock Symbol must be 1-5 letters long. Minimum % Change must be 7.'
    return render_template('templates_user_logged_in/loggedin_home_page.html', error_message_from_python_to_html = output_message)
  else:
    # Create uuid and timestamp for insertion
    user_table_insert_uuid = create_uuid_function()
    user_track_symbol_timestamp = create_timestamp_function()
    # Database
    connection_postgres, cursor = connect_to_postgres_function()
    error_message_check_if_exist = select_stock_tracking_table_duplicates_function(connection_postgres, cursor, session['logged_in_user_uuid'], user_symbol_from_html_form_sanitized)
    if error_message_check_if_exist == 'none':
      output_message = insert_stock_tracking_table_function(connection_postgres, cursor, user_table_insert_uuid, user_track_symbol_timestamp, user_symbol_from_html_form_sanitized, user_symbol_percent_change_from_html_form_sanitized, session['logged_in_user_uuid'])
    else:
      output_message = error_message_check_if_exist
      return render_template('templates_user_logged_in/loggedin_home_page.html', error_message_from_python_to_html = output_message)
    close_connection_cursor_to_database_function(connection_postgres, cursor)
    return render_template('templates_user_logged_in/loggedin_home_page.html', error_message_from_python_to_html = output_message)