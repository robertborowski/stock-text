from flask import render_template, Blueprint, session, redirect, request
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function
from backend.utils.app_before_setup.check_if_url_www import check_if_url_www_function
from backend.utils.app_before_setup.remove_www_from_domain import remove_www_from_domain_function

account_page_edit_information = Blueprint("account_page_edit_information", __name__, static_folder="static", template_folder="templates")

@account_page_edit_information.before_request
def before_request():
  """Returns: The domain should work with both www and non-www domain"""
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=301)

@account_page_edit_information.route("/account/edit", methods=["POST", "GET"])
def account_page_edit_information_function():
  """Returns: Renders the user's account page"""
  if session['logged_in_user_email'] != 'none':
    return render_template('templates_user_logged_in/account_edit_information.html',
                            user_email_from_session_to_html = session['logged_in_user_email'],
                            user_first_name_from_session_to_html = session['logged_in_user_first_name'],
                            user_last_name_from_session_to_html = session['logged_in_user_last_name'],
                            user_phone_number_from_session_to_html = session['logged_in_user_phone_number'])
  else:
    set_session_variables_to_none_logout_function()
    return redirect("https://symbolnews.com/", code=301)