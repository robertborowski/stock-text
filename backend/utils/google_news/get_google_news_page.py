import pyshorteners

def get_google_news_page_function(input_search_name):
  """
  Returns: Search company name on google
  """
  search_long_url = "https://www.google.com/search?q=" + input_search_name + "&safe=strict&source=lnms&tbm=nws"
  shortener = pyshorteners.Shortener()
  search_short_url = shortener.tinyurl.short(search_long_url)
  return search_short_url