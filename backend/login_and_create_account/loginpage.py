from flask import render_template, Blueprint, session, url_for, redirect
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function
from backend.user_logged_in.home.homepage import homepage

loginpage = Blueprint("loginpage", __name__, static_folder="static", template_folder="templates")
@loginpage.route("/")
def index_function():
  """
  Returns: Renders the login page
  """
  if session.get('logged_in_user_email') == True:
    print(session['logged_in_user_email'])
    return redirect(url_for('homepage.logged_in_home_page_function'))
  else:
    #set_session_variables_to_none_logout_function()
    return render_template('templates_login_and_create_account/index.html')