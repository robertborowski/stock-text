from flask import render_template, Blueprint, session
logout = Blueprint("logout", __name__, static_folder="static", template_folder="templates")
@logout.route("/log_out", methods=["POST", "GET"])
def logout_function():
  """
  Returns: renders page for the URL decorator
  """
  if session['logged_in_user_email'] != 'none':
    session['logged_in_user_uuid'] = 'none'
    session['logged_in_user_email'] = 'none'
    session['logged_in_user_first_name'] = 'none'
    session['logged_in_user_last_name'] = 'none'
    session['logged_in_user_phone_number'] = 'none'
    return render_template('templates_login_and_create_account/index.html')
  else:
    session['logged_in_user_uuid'] = 'none'
    session['logged_in_user_email'] = 'none'
    session['logged_in_user_first_name'] = 'none'
    session['logged_in_user_last_name'] = 'none'
    session['logged_in_user_phone_number'] = 'none'
    return render_template('templates_login_and_create_account/index.html')