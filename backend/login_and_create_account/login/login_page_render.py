from flask import render_template, Blueprint, session, redirect, request
from backend.utils.app_before_setup.check_if_url_www import check_if_url_www_function
from backend.utils.app_before_setup.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.create_uuid import create_uuid_function

login_page_render = Blueprint("login_page_render", __name__, static_folder="static", template_folder="templates")

@login_page_render.before_request
def before_request():
  """Returns: The domain should work with both www and non-www domain"""
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=301)

@login_page_render.route("/login")
def login_page_render_function():  
  """Returns: The login page"""
  # Need to create a css unique key so that cache busting can be done
  css_cache_busting_variable = create_uuid_function('css_')
  
  # Check if user session data is already present/signed in
  if session and session.get('logged_in_user_email') != 'none':
    return redirect('https://symbolnews.com/dashboard', code=301)
  
  # When redirected to this page, first check if there is an session error message associated with this redirect
  if session and session.get('output_message_login_page_session') != None:
    # Set the variables based on session inputs
    output_message_login_page = session['output_message_login_page_session']
    
    try:
      return render_template('templates_login_and_create_account/login_page.html', output_message_from_python_to_html = output_message_login_page, css_cache_busting_variable_to_html = css_cache_busting_variable)
    except:
      return 'failed'
    finally:
      session['output_message_login_page_session'] = None
  
  # If no error message than just render as per usual
  else:
    return render_template('templates_login_and_create_account/login_page.html', css_cache_busting_variable_to_html = css_cache_busting_variable)