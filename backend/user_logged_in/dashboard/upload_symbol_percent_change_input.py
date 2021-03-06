from flask import render_template, Blueprint, session, request, redirect
from backend.utils.sanitize_user_inputs.sanitize_symbol_input import sanitize_symbol_input_function
from backend.utils.sanitize_user_inputs.sanitize_symbol_percent_change_input import sanitize_symbol_percent_change_input_function
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.queries.insert_queries.insert_stock_tracking_table import insert_stock_tracking_table_function
from backend.db.queries.insert_queries.insert_stock_news_links_table import insert_stock_news_links_table_function
from backend.db.queries.insert_queries.insert_jobs_queues_table import insert_jobs_queues_table_function
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
  if session and session.get('logged_in_user_email') != 'none':
    # Sanitize/confirm user inputs
    user_symbol_from_html_form_sanitized = sanitize_symbol_input_function(request.form.get('track_symbol'))
    does_symbol_exist = yfinance_check_if_symbol_exists_function(user_symbol_from_html_form_sanitized)
    user_symbol_percent_change_from_html_form_sanitized = sanitize_symbol_percent_change_input_function(request.form.get('track_percent_change'))
    
    # If user inputs were invalid
    if user_symbol_from_html_form_sanitized == 'none' or does_symbol_exist == 'none' or user_symbol_percent_change_from_html_form_sanitized == 'none':
      session['output_message_dashboard_page_session'] = 'Stock Symbol must exist and be 1-5 letters long. Minimum % Change must be 7.'
      return redirect("https://symbolnews.com/dashboard", code=301)

    # If user inputs were valid
    else:
      # Create uuid and timestamp for insertion
      user_table_insert_uuid = create_uuid_function("symt_")
      user_track_symbol_timestamp = create_timestamp_function()

      # Database insert
      connection_postgres, cursor = connect_to_postgres_function()
      # Check if user is already tracking this symbol
      error_message_check_if_exist = select_stock_tracking_table_duplicates_function(connection_postgres, cursor, session['logged_in_user_uuid'], user_symbol_from_html_form_sanitized)
      
      # If user is not already tracking this symbol
      if error_message_check_if_exist == 'none':
        # Insert stock tracking information into the stock_tracking_table
        session['output_message_dashboard_page_session'] = insert_stock_tracking_table_function(connection_postgres, cursor, user_table_insert_uuid, user_track_symbol_timestamp, user_symbol_from_html_form_sanitized, user_symbol_percent_change_from_html_form_sanitized, session['logged_in_user_uuid'])

        # Get google news link for the symbol not company short name yet, a job will get the short name in order to save wait time for user
        temporary_google_search_input = user_symbol_from_html_form_sanitized + '_stock'
        google_news_url_link = get_google_news_page_function(temporary_google_search_input)

        # Insert into the new stock_news_links_table the 1.symbol and 2.google_link(symbol search)
        try:
          output_message_news_link_upload = insert_stock_news_links_table_function(connection_postgres, cursor, user_symbol_from_html_form_sanitized, google_news_url_link)
        except:
          pass

        # Insert into job/queue table so that the job can get the company short name every 10 min in the background
        try:
          job_queue_name = 'get_company_short_name'
          output_message_job_upload = insert_jobs_queues_table_function(connection_postgres, cursor, job_queue_name, user_symbol_from_html_form_sanitized)
        except:
          pass
        return redirect("/dashboard", code=301)
        #return redirect("https://symbolnews.com/dashboard", code=301)
      
      # If user is already tracking this symbol
      else:
        session['output_message_dashboard_page_session'] = error_message_check_if_exist
        return redirect("/dashboard", code=301)
        #return redirect("https://symbolnews.com/dashboard", code=301)

  # If no session info found
  else:
    set_session_variables_to_none_logout_function()
    return redirect("https://symbolnews.com/", code=301)