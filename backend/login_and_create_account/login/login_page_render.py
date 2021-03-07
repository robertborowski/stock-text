from flask import render_template, Blueprint, session, url_for, redirect, request
from backend.utils.app_before_setup.check_if_url_www import check_if_url_www_function
from backend.utils.app_before_setup.remove_www_from_domain import remove_www_from_domain_function

login_page_render = Blueprint("login_page_render", __name__, static_folder="static", template_folder="templates")

@login_page_render.before_request
def before_request():
  """Returns: The domain should work with both www and non-www domain"""
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=301)

@login_page_render.route("/")
def login_page_render_function():
  """Returns: Renders the login page"""
  # When redirected to this page, first check if there is an session error message associated with this redirect
  if session and session.get('login_failed_message') != None:
    try:
      return render_template('templates_login_and_create_account/login_page.html', error_message_from_python_to_html = session['login_failed_message'])
    except:
      return 'failed'
    finally:
      session['login_failed_message'] = None
  
  # If no error message than just render as per usual
  else:
    return render_template('templates_login_and_create_account/login_page.html')