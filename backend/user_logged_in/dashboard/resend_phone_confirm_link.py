from flask import Flask, redirect, url_for, request, session, Blueprint
import os
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function
from backend.utils.app_before_setup.check_if_url_www import check_if_url_www_function
from backend.utils.app_before_setup.remove_www_from_domain import remove_www_from_domain_function
from backend.login_and_create_account.create_confirm_token import create_confirm_token_function
from backend.user_logged_in.confirm.confirm_email_page import confirm_email_page
from backend.user_logged_in.confirm.confirm_email_page import confirm_email_page_function
from backend.utils.constant_run.twilio.send_email_confirm_account import send_email_confirm_account_function
from backend.utils.constant_run.twilio.send_phone_number_confirm_account import send_phone_number_confirm_account_function

resend_phone_confirm_link = Blueprint("resend_phone_confirm_link", __name__, static_folder="static", template_folder="templates")

@resend_phone_confirm_link.before_request
def before_request():
  """Returns: The domain should work with both www and non-www domain"""
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=301)

@resend_phone_confirm_link.route("/resend_phone_confirm_link", methods=["POST", "GET"])
def resend_phone_confirm_link_function():
  """Returns: Uploads new account info to Postgres database, if it does not already exist."""
  if session and session.get('logged_in_user_email') != 'none':
    # Set session variables
    user_phone_number = session.get('logged_in_user_phone_number')
    user_first_name = session.get('logged_in_user_first_name')

    # Create tokens for email and phone number verification
    confirm_phone_number_token = create_confirm_token_function(user_phone_number, os.environ.get('URL_SAFE_SERIALIZER_SECRET_KEY_EMAIL'), os.environ.get('URL_SAFE_SERIALIZER_SECRET_SALT_EMAIL'))
    
    # Create the URL links for email and phone number verification
    url_for('confirm_phone_number_page.confirm_phone_number_page_function', confirm_phone_number_token_url_variable = confirm_phone_number_token)

    # Send the confirmation email and text links to user
    send_phone_number_confirm_account_function(user_phone_number, user_first_name, confirm_phone_number_token)

    # Set output message for dashboard
    session['dashboard_upload_output_message'] = "Phone confirm link resent! Search for word SymbolNews."

    # Redirect to page
    return redirect("https://symbolnews.com/dashboard", code=301)

  else:
    set_session_variables_to_none_logout_function()
    return redirect("https://symbolnews.com/", code=301)
  return redirect("https://symbolnews.com/", code=301)