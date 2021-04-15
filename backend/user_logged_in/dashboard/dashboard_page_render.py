from flask import render_template, Blueprint, session, request, redirect
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.queries.select_queries.select_user_tracking_list import select_user_tracking_list_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function
from backend.utils.app_before_setup.check_if_url_www import check_if_url_www_function
from backend.utils.app_before_setup.remove_www_from_domain import remove_www_from_domain_function
from backend.db.queries.select_queries.select_user_confirmed_account_status import select_user_confirmed_account_status_function
from backend.utils.create_uuid import create_uuid_function

dashboard_page_render = Blueprint("dashboard_page_render", __name__, static_folder="static", template_folder="templates")

@dashboard_page_render.before_request
def before_request():
  """Returns: The domain should work with both www and non-www domain"""
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=301)

@dashboard_page_render.route("/dashboard", methods=["POST", "GET"])
def dashboard_page_render_function():
  """Returns: User dashboard with user symbol tracking list"""
  # Need to create a css unique key so that cache busting can be done
  css_cache_busting_variable = create_uuid_function('css_')

  if session and session.get('logged_in_user_email') != 'none' and session.get('logged_in_user_email') != None:
    # Get info for the page render
    # Connect to database
    connection_postgres, cursor = connect_to_postgres_function()
    
    # Pull tracking list from databse
    symbol_tracking_list = select_user_tracking_list_function(connection_postgres, cursor, session['logged_in_user_uuid'])
    # Check if email and phone number are verified
    display_output_message_email, display_output_message_phone_number = select_user_confirmed_account_status_function(connection_postgres, cursor, session['logged_in_user_uuid'])

    # If not verified yet, unhide the resend link text
    resend_email_confirm_link = ''
    resend_phone_number_confirm_link = ''

    # Add the resend link text words to html file if they are not blank/None
    if display_output_message_email != None and len(display_output_message_email) >= 2:
      resend_email_confirm_link = 'Click to resend email confirmation link.'
    if display_output_message_phone_number != None and len(display_output_message_phone_number) >= 2:
      resend_phone_number_confirm_link = 'Click to resend phone number confirmation link.'

    # Close the connnection to database
    close_connection_cursor_to_database_function(connection_postgres, cursor)
    
    # When redirected to this page, first check if there is an session error message associated with this redirect
    if session and session.get('output_message_dashboard_page_session') != None:
      try:
        return render_template('templates_user_logged_in/loggedin_dashboard_page.html',
                            user_email_from_session_to_html = session['logged_in_user_email'],
                            user_first_name_from_session_to_html = session['logged_in_user_first_name'],
                            user_last_name_from_session_to_html = session['logged_in_user_last_name'],
                            user_phone_number_from_session_to_html = session['logged_in_user_phone_number'],
                            symbol_tracking_list_from_python_to_html = symbol_tracking_list,
                            output_message_from_python_to_html = session['output_message_dashboard_page_session'],
                            resend_email_confirm_link_to_html = resend_email_confirm_link,
                            resend_phone_number_confirm_link_to_html = resend_phone_number_confirm_link,
                            css_cache_busting_variable_to_html = css_cache_busting_variable)
      except:
        return 'failed'
      finally:
        session['output_message_dashboard_page_session'] = None
    

    # Render the page
    return render_template('templates_user_logged_in/loggedin_dashboard_page.html',
                            user_email_from_session_to_html = session['logged_in_user_email'],
                            user_first_name_from_session_to_html = session['logged_in_user_first_name'],
                            user_last_name_from_session_to_html = session['logged_in_user_last_name'],
                            user_phone_number_from_session_to_html = session['logged_in_user_phone_number'],
                            symbol_tracking_list_from_python_to_html = symbol_tracking_list,
                            resend_email_confirm_link_to_html = resend_email_confirm_link,
                            resend_phone_number_confirm_link_to_html = resend_phone_number_confirm_link,
                            css_cache_busting_variable_to_html = css_cache_busting_variable)

  # If no session info found
  else:
    set_session_variables_to_none_logout_function()
    return redirect("https://symbolnews.com/", code=301)