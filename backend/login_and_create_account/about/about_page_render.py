from flask import render_template, Blueprint, redirect, request, session
from backend.utils.app_before_setup.check_if_url_www import check_if_url_www_function
from backend.utils.app_before_setup.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.create_uuid import create_uuid_function

about_page_render = Blueprint("about_page_render", __name__, static_folder="static", template_folder="templates")

@about_page_render.before_request
def before_request():
  """Returns: The domain should work with both www and non-www domain"""
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=301)

@about_page_render.route("/about")
def about_page_render_function():
  """Returns: Renders the create account page"""
  # Need to create a css unique key so that cache busting can be done
  css_cache_busting_variable = create_uuid_function('css_')
  
  return render_template('templates_login_and_create_account/about_page.html', css_cache_busting_variable_to_html = css_cache_busting_variable)