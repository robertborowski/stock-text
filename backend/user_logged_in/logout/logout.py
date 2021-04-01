from flask import render_template, Blueprint, session, redirect
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function

logout = Blueprint("logout", __name__, static_folder="static", template_folder="templates")
@logout.route("/log_out", methods=["POST", "GET"])
def logout_function():
  """
  Returns: Logs out of account
  """
  if session and session.get('logged_in_user_email') != 'none':
    set_session_variables_to_none_logout_function()
    session['output_message_landing_page_session'] = 'Logged out'
    return redirect("https://symbolnews.com/", code=301)
  else:
    set_session_variables_to_none_logout_function()
    return redirect("https://symbolnews.com/", code=301)