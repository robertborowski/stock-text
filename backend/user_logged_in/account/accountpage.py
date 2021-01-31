from flask import render_template, Blueprint, session
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function
accountpage = Blueprint("accountpage", __name__, static_folder="static", template_folder="templates")
@accountpage.route("/account", methods=["POST", "GET"])
def account_page_function():
  """
  Returns: Renders the user's account page
  """
  if session['logged_in_user_email'] != 'none':
    return render_template('templates_user_logged_in/account.html',
                            user_email_from_session_to_html = session['logged_in_user_email'],
                            user_first_name_from_session_to_html = session['logged_in_user_first_name'],
                            user_last_name_from_session_to_html = session['logged_in_user_last_name'],
                            user_phone_number_from_session_to_html = session['logged_in_user_phone_number'])
  else:
    set_session_variables_to_none_logout_function()
    return render_template('templates_login_and_create_account/index.html')