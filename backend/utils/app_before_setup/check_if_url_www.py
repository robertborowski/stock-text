from urllib.parse import urlparse, urlunparse

def check_if_url_www_function(current_url):
  """
  Returns: Checks if current URL starts with www.
  """
  urlparts = urlparse(current_url)
  if urlparts.netloc == 'www.symbolnews.com':
    print('---------------------------------')
    print(urlparts.netloc)
    print('---------------------------------')
    return True
  return False