from flask import render_template, Blueprint, session, request, redirect
from backend.utils.sanitize_user_inputs.sanitize_symbol_input import sanitize_symbol_input_function
from backend.utils.sanitize_user_inputs.sanitize_symbol_percent_change_input import sanitize_symbol_percent_change_input_function
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.queries.insert_queries.insert_stock_tracking_table import insert_stock_tracking_table_function
from backend.utils.create_uuid import create_uuid_function
from backend.utils.create_timestamp import create_timestamp_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.db.queries.select_queries.select_stock_tracking_table_duplicates import select_stock_tracking_table_duplicates_function
from backend.utils.yfinance.yfinance_check_if_symbol_exists import yfinance_check_if_symbol_exists_function
from backend.db.queries.select_queries.select_user_tracking_list import select_user_tracking_list_function
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function
from backend.utils.google_news.get_google_news_page import get_google_news_page_function
from backend.utils.yfinance.get_company_short_name import get_company_short_name_function
from backend.utils.app_before_setup.check_if_url_www import check_if_url_www_function
from backend.utils.app_before_setup.remove_www_from_domain import remove_www_from_domain_function

upload_symbol_percent_change_input = Blueprint("upload_symbol_percent_change_input", __name__, static_folder="static", template_folder="templates")

@upload_symbol_percent_change_input.before_request
def before_request():
  """Returns: The domain should work with both www and non-www domain"""
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=301)

@upload_symbol_percent_change_input.route("/dashboard/uploaded", methods=["POST", "GET"])
def upload_symbol_percent_change_input_function():
  """Returns: sanatizes the user input, then uploads it into the database and data table"""
  if session['logged_in_user_email'] != 'none':
    # Sanitize/confirm user inputs
    user_symbol_from_html_form_sanitized = sanitize_symbol_input_function(request.form.get('track_symbol'))
    does_symbol_exist = yfinance_check_if_symbol_exists_function(user_symbol_from_html_form_sanitized)
    user_symbol_percent_change_from_html_form_sanitized = sanitize_symbol_percent_change_input_function(request.form.get('track_percent_change'))
    
    # If user inputs were invalid
    if user_symbol_from_html_form_sanitized == 'none' or does_symbol_exist == 'none' or user_symbol_percent_change_from_html_form_sanitized == 'none':
      session['dashboard_upload_output_message'] = 'Stock Symbol must exist and be 1-5 letters long. Minimum % Change must be 7.'
      return redirect("https://symbolnews.com/dashboard", code=301)

    # If user inputs were valid
    else:
      # Create uuid and timestamp for insertion
      user_table_insert_uuid = create_uuid_function("symt")
      user_track_symbol_timestamp = create_timestamp_function()

      # Database insert
      connection_postgres, cursor = connect_to_postgres_function()
      # Check if user is already tracking this symbol
      error_message_check_if_exist = select_stock_tracking_table_duplicates_function(connection_postgres, cursor, session['logged_in_user_uuid'], user_symbol_from_html_form_sanitized)
      
      # If user is not already tracking this symbol
      if error_message_check_if_exist == 'none':
        company_short_name_without_spaces = get_company_short_name_function(user_symbol_from_html_form_sanitized)
        google_news_url_link = get_google_news_page_function(company_short_name_without_spaces)
        session['dashboard_upload_output_message'] = insert_stock_tracking_table_function(connection_postgres, cursor, user_table_insert_uuid, user_track_symbol_timestamp, user_symbol_from_html_form_sanitized, user_symbol_percent_change_from_html_form_sanitized, session['logged_in_user_uuid'], google_news_url_link)
        return redirect("https://symbolnews.com/dashboard", code=301)
      
      # If user is already tracking this symbol
      else:
        session['dashboard_upload_output_message'] = error_message_check_if_exist
        return redirect("https://symbolnews.com/dashboard", code=301)

  # If no session info found
  else:
    set_session_variables_to_none_logout_function()
    return redirect("https://symbolnews.com/", code=301)