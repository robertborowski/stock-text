from flask import render_template, Blueprint, session, url_for, redirect, request
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function
from backend.user_logged_in.home.homepage import homepage

loginpage = Blueprint("loginpage", __name__, static_folder="static", template_folder="templates")

# Load app URL
@loginpage.route("/")
def index_function():
  """
  Returns: Renders the login page
  """
  if session and 'logged_in_user_email' in session and session.get('logged_in_user_email') != 'none':
    session.permanent = True
    return redirect("https://symbolnews.com/home", code=301)
  else:
    #set_session_variables_to_none_logout_function()
    return render_template('templates_login_and_create_account/index.html')