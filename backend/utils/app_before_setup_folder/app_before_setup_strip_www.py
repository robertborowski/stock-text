from flask import render_template, Blueprint, session, request, redirect
from urllib.parse import urlparse, urlunparse

def app_before_setup_strip_www_function():
  """
  Returns: Redirect www requests to non-www.
  """
  url_to_search = 'www.symbolnews.com'
  urlparts = urlparse(request.url)
  print('- - - - 1 - - - - - ')
  print(type(urlparts))
  print(urlparts)
  print('- - - - 1 - - - - - ')
  if urlparts.netloc == url_to_search:
    urlparts_list = list(urlparts)
    urlparts_list[1] = 'symbolnews.com'
    print('- - - - 2 - - - - - ')
    print(urlparts_list)
    print('- - - - 2 - - - - - ')
    return redirect(urlunparse(urlparts_list), code=301)