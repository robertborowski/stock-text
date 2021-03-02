from flask import render_template, Blueprint, session

loginpage = Blueprint("loginpage", __name__, static_folder="static", template_folder="templates")
@loginpage.route("/")
def index_function():
  """
  Returns: Renders the login page
  """
  if session['logged_in_user_email'] != 'none':
    return render_template('templates_user_logged_in/loggedin_home_page.html')
  else:
    return render_template('templates_login_and_create_account/index.html')