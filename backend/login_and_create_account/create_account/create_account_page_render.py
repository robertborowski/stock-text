from flask import render_template, Blueprint, redirect, request, session
from backend.utils.app_before_setup.check_if_url_www import check_if_url_www_function
from backend.utils.app_before_setup.remove_www_from_domain import remove_www_from_domain_function

create_account_page_render = Blueprint("create_account_page_render", __name__, static_folder="static", template_folder="templates")

@create_account_page_render.before_request
def before_request():
  """Returns: The domain should work with both www and non-www domain"""
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=301)

@create_account_page_render.route("/create_account")
def create_account_page_render_function():
  """Returns: Renders the create account page"""
  # When redirected to this page, first check if there is an session error message associated with this redirect
  if session and session.get('create_account_failed_message') != None:
    try:
      return render_template('templates_login_and_create_account/create_account_page.html', error_message_from_python_to_html = session['create_account_failed_message'])
    except:
      return 'failed'
    finally:
      session['create_account_failed_message'] = None
  
  # If no error message than just render as per usual
  else:
    return render_template('templates_login_and_create_account/create_account_page.html')