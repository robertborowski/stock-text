from flask import render_template, Blueprint, session, request, redirect
from urllib.parse import urlparse, urlunparse

def app_before_setup_function():
  #def strip_www_function():
  """
  Returns: Redirect www requests to non-www.
  """
  url_to_search = 'www.symbolnews.com'
  urlparts = urlparse(request.url)
  if urlparts.netloc == url_to_search:
    urlparts_list = list(urlparts)
    urlparts_list[1] = 'symbolnews.com'
    return redirect(urlunparse(urlparts_list), code=301)
  
  # strip the www from the URL
  #strip_www_function()