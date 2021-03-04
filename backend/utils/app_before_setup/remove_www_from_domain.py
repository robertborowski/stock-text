from flask import render_template, Blueprint, session, request, redirect
from urllib.parse import urlparse, urlunparse

def remove_www_from_domain_function(current_url):
  """
  Returns: Redirect www requests to non-www.
  """
  urlparts = urlparse(current_url)
  print('- - - - 1 - - - - - ')
  print(urlparts)
  print('- - - - 1 - - - - - ')
  if urlparts.netloc == 'www.symbolnews.com':
    urlparts_list = list(urlparts)
    urlparts_list[1] = 'symbolnews.com'
    print('- - - - 2 - - - - - ')
    print(urlunparse(urlparts_list))
    print('- - - - 2 - - - - - ')
    return urlunparse(urlparts_list)