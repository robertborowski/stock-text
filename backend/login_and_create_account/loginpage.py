from flask import render_template, Blueprint, session, url_for, redirect
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function
from backend.user_logged_in.home.homepage import homepage
from backend.utils.redirect_url.naked_url import naked_url_function

loginpage = Blueprint("loginpage", __name__, static_folder="static", template_folder="templates")
@loginpage.route("/")
def index_function():
  """
  Returns: Renders the login page
  """
  """
  print('- - - - - -BEFORE NAKED loginpage - - - - - - -')
  naked_url_function("/")
  print('- - - - - -AFTER NAKED loginpage - - - - - - -')
  """
  if session and 'logged_in_user_email' in session and session.get('logged_in_user_email') != 'none':
    return redirect("https://www.symbolnews.com/home", code=302)
  else:
    #set_session_variables_to_none_logout_function()
    return render_template('templates_login_and_create_account/index.html')