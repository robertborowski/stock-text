from flask import render_template, Blueprint, session, url_for, redirect, request
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function
from backend.user_logged_in.home.homepage import homepage
from backend.utils.app_before_setup.check_if_url_www import check_if_url_www_function
from backend.utils.app_before_setup.remove_www_from_domain import remove_www_from_domain_function

loginpage = Blueprint("loginpage", __name__, static_folder="static", template_folder="templates")

@loginpage.before_request
def before_request():
  # Domain Check #1 - Does it start with www.
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    # Redirect page to non-www
    return redirect(new_url, code=301)

@loginpage.route("/")
def index_function():
  """
  Returns: Renders the login page
  """
  # If session info found
  #if session and 'logged_in_user_email' in session and session.get('logged_in_user_email') != 'none':
  if session and 'logged_in_user_email' in session and (session.get('logged_in_user_email') != 'none' or session.get('logged_in_user_email') != "temp_placeholder_email@symbolnews.com" or session.get('logged_in_user_email') != None):
    session.permanent = True
    print('- - - - - - - - -')
    print(session.get('logged_in_user_email'))
    print('- - - - - - - - -')
    return redirect("https://symbolnews.com/home", code=301)
  
  # If no session info found
  else:
    set_session_variables_to_none_logout_function()
    return render_template('templates_login_and_create_account/index.html')