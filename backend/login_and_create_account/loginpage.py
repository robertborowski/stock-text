from flask import render_template, Blueprint

loginpage = Blueprint("loginpage", __name__, static_folder="static", template_folder="templates")
@loginpage.route("/")
def index_function():
  """
  Returns: Renders the login page
  """
  return render_template('templates_login_and_create_account/index.html')