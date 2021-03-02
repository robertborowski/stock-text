from flask import render_template, Blueprint, session, request, redirect
from urllib.parse import urlparse, urlunparse

def naked_url_function(ext_sub_page):
  """
  Returns: Redirect non-www requests to www.
  """
  urlparts = urlparse(request.url)
  if urlparts.netloc == 'symbolnews.com' + ext_sub_page:
    urlparts_list = list(urlparts)
    urlparts_list[1] = 'www.symbolnews.com' + ext_sub_page
    return redirect(urlunparse(urlparts_list), code=301)
  return request.url