from flask import render_template, Blueprint, session, redirect, request
from backend.utils.set_session_variables_to_none_logout import set_session_variables_to_none_logout_function
from backend.utils.app_before_setup.check_if_url_www import check_if_url_www_function
from backend.utils.app_before_setup.remove_www_from_domain import remove_www_from_domain_function

delete_account_page_render = Blueprint("delete_account_page_render", __name__, static_folder="static", template_folder="templates")

@delete_account_page_render.before_request
def before_request():
  """Returns: The domain should work with both www and non-www domain"""
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=301)

@delete_account_page_render.route("/account/delete", methods=["POST", "GET"])
def delete_account_page_render_function():
  if session and 'logged_in_user_email' in session and session.get('logged_in_user_email') != 'none':
    return render_template('templates_user_logged_in/account_delete.html')
  else:
    set_session_variables_to_none_logout_function()
    return redirect("https://symbolnews.com/", code=301)