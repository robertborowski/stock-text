from flask import render_template, Blueprint, session, url_for, redirect, request
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function
from backend.user_logged_in.home.homepage import homepage
from urllib.parse import urlparse, urlunparse
from backend.utils.app_before_setup_folder.app_before_setup import app_before_setup_function

loginpage = Blueprint("loginpage", __name__, static_folder="static", template_folder="templates")
@loginpage.before_request
def before_request_function():
  return app_before_setup_function()
@loginpage.route("/")
def index_function():
  """
  Returns: Renders the login page
  """
  if session and 'logged_in_user_email' in session and session.get('logged_in_user_email') != 'none':
    return redirect("https://symbolnews.com/home", code=302)
  else:
    #set_session_variables_to_none_logout_function()
    return render_template('templates_login_and_create_account/index.html')