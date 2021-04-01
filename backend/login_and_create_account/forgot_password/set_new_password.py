from flask import Flask, redirect, url_for, render_template, request, session, Blueprint, current_app
from itsdangerous import URLSafeTimedSerializer
import os
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.utils.app_before_setup.check_if_url_www import check_if_url_www_function
from backend.utils.app_before_setup.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.create_uuid import create_uuid_function

set_new_password = Blueprint("set_new_password", __name__, static_folder="static", template_folder="templates")

@set_new_password.before_request
def before_request():
  """Returns: The domain should work with both www and non-www domain"""
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=301)

@set_new_password.route("/set_new_password/<confirm_email_token_url_variable>", methods=["POST", "GET"])
def set_new_password_function(confirm_email_token_url_variable):
  """Returns: confirms email token link"""
  # Need to create a css unique key so that cache busting can be done
  css_cache_busting_variable = create_uuid_function('css_')

  # Check if user session data is already present/signed in
  if session and session.get('logged_in_user_email') != 'none':
    return redirect('https://symbolnews.com/dashboard', code=301)
    
  # Setup token serializer
  serializer_instance = URLSafeTimedSerializer(os.environ.get('URL_SAFE_SERIALIZER_SECRET_KEY_EMAIL'))
  string_to_salt = os.environ.get('URL_SAFE_SERIALIZER_SECRET_SALT_EMAIL').encode("utf-8")
  
  # See if token matches the one sent out
  try:
    user_email_confirming = serializer_instance.loads(confirm_email_token_url_variable, salt=string_to_salt, max_age=3600)
    session['user_email_to_change_password'] = user_email_confirming
    return render_template('templates_login_and_create_account/new_password_page.html', css_cache_busting_variable_to_html = css_cache_busting_variable)
  
  # If token does not match the one sent out
  except:
    session['output_message_landind_page_session'] = 'Token has expired!'
    return redirect("https://symbolnews.com/", code=301)
  return redirect("https://symbolnews.com/", code=301)