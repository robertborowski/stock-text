from flask import render_template, Blueprint, redirect, request, session
from backend.utils.app_before_setup.check_if_url_www import check_if_url_www_function
from backend.utils.app_before_setup.remove_www_from_domain import remove_www_from_domain_function

forgot_password_render_page = Blueprint("forgot_password_render_page", __name__, static_folder="static", template_folder="templates")
@forgot_password_render_page.route("/forgot_password")
def forgot_password_render_page_function():
  """
  Returns: Renders the create account page
  """
  # Domain Check #1 - Does it start with www.
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    # Redirect page to non-www
    return redirect(new_url, code=301)

  # # If session info found
  if session and 'logged_in_user_email' in session and session.get('logged_in_user_email') != 'none':
    session.permanent = True
    return redirect("https://symbolnews.com/home", code=301)

  return render_template('templates_login_and_create_account/forgot_password_page.html')