from flask import render_template, Blueprint, session
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function

delete_account_page = Blueprint("delete_account_page", __name__, static_folder="static", template_folder="templates")
@delete_account_page.route("/account/delete", methods=["POST", "GET"])
def delete_account_page_function():
  if session['logged_in_user_email'] != 'none':
    return render_template('templates_user_logged_in/account_delete.html')
  else:
    set_session_variables_to_none_logout_function()
    return render_template('templates_login_and_create_account/index.html')