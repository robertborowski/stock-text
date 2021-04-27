from flask import render_template, Blueprint, session, redirect, request
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.utils.app_before_setup.check_if_url_www import check_if_url_www_function
from backend.utils.app_before_setup.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.constant_run.twilio.send_email_account_deleted import send_email_account_deleted_function
from backend.db.queries.update_queries.update_user_delete_account_requested_true import update_user_delete_account_requested_true_function

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
  """Returns: Deletes all symbols associated with an account and then deletes the account itself as well"""
  if session['logged_in_user_email'] != 'none':
    # Set the incoming session variables
    user_email = session['logged_in_user_email']
    user_first_name = session['logged_in_user_first_name']

    # Connect to database
    connection_postgres, cursor = connect_to_postgres_function()
    
    # Mark account for deletion
    update_user_delete_account_requested_true_function(connection_postgres, cursor, session['logged_in_user_uuid'])

    # Send account deleted email
    send_email_account_deleted_function(user_email, user_first_name)
    
    # Close database connection
    close_connection_cursor_to_database_function(connection_postgres, cursor)
    
    # Set all session variables to none
    set_session_variables_to_none_logout_function()
    
    # Set outgoing session variables
    session['output_message_landing_page_session'] = 'Account deleted!'
    
    # Redirect to landing page
    return redirect("https://symbolnews.com/", code=301)
  
  else:
    set_session_variables_to_none_logout_function()
    return redirect("https://symbolnews.com/", code=301)