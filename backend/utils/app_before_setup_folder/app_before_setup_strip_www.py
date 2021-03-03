from flask import render_template, Blueprint, session, request, redirect
from urllib.parse import urlparse, urlunparse

def app_before_setup_strip_www_function(extension_url):
  """
  Returns: Redirect www requests to non-www.
  """
  url_to_search = 'www.symbolnews.com' + extension_url
  urlparts = urlparse(request.url)
  print('- - - - - - - - - ')
  print(urlparts)
  print('- - - - - - - - - ')
  if urlparts.netloc == url_to_search:
    urlparts_list = list(urlparts)
    urlparts_list[1] = 'symbolnews.com' + extension_url
    return redirect(urlunparse(urlparts_list), code=301) 