from flask import render_template, Blueprint, session, url_for, redirect
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function
from backend.user_logged_in.home.homepage import homepage

loginpage = Blueprint("loginpage", __name__, static_folder="static", template_folder="templates")
@loginpage.route("/")
def index_function():
  """
  Returns: Renders the login page
  """
  print('- - - - 1- - - -')
  print(session)
  print('- - - - 1- - - -')
  if session and 'logged_in_user_email' in session:
    print('- - - -2 - - - -')
    print(session['logged_in_user_email'])
    print('- - - - 2- - - -')
    return redirect("symbolnews.com/home", code=302)
  else:
    #set_session_variables_to_none_logout_function()
    return render_template('templates_login_and_create_account/index.html')