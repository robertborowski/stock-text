from flask import render_template, Blueprint, session, url_for, redirect
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function

loginpage = Blueprint("loginpage", __name__, static_folder="static", template_folder="templates")
@loginpage.route("/")
def index_function():
  """
  Returns: Renders the login page
  """
  if session.get('logged_in_user_email') == True:
    return redirect(url_for('/home'))
  else:
    #set_session_variables_to_none_logout_function()
    return render_template('templates_login_and_create_account/index.html')