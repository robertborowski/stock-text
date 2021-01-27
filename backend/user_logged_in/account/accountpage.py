from flask import render_template, Blueprint, session
accountpage = Blueprint("accountpage", __name__, static_folder="static", template_folder="templates")
@accountpage.route("/account", methods=["POST", "GET"])
def account_page_function():
  """
  Returns: Renders the user's account page
  """
  if session['logged_in_user_email'] != 'none':
    print('Status: Function End:[account_page_function]')
    return render_template('templates_user_logged_in/account.html',
                            user_email_from_session_to_html = session['logged_in_user_email'],
                            user_name_from_session_to_html = session['logged_in_user_name'],
                            user_phone_number_from_session_to_html = session['logged_in_user_phone_number'])
  else:
    session['logged_in_user_email'] = 'none'
    session['logged_in_user_name'] = 'none'
    session['logged_in_user_phone_number'] = 'none'
    return render_template('templates_login_and_create_account/index.html')