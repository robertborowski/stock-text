from flask import render_template, Blueprint, session
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function

logout = Blueprint("logout", __name__, static_folder="static", template_folder="templates")
@logout.route("/log_out", methods=["POST", "GET"])
def logout_function():
  """
  Returns: Logs out of account
  """
  if session['logged_in_user_email'] != 'none':
    set_session_variables_to_none_logout_function()
    return render_template('templates_login_and_create_account/index.html')
  else:
    set_session_variables_to_none_logout_function()
    return render_template('templates_login_and_create_account/index.html')