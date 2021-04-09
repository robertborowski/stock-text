import yfinance as yf
from backend.utils.google_news.get_google_news_page import get_google_news_page_function

def get_latest_symbol_info_function(input_set):
  """
  Returns: Latest stock symbol information as dict
  """
  symbol_lookup_dict = {}
  for sym in input_set:
    try:
      ticker = yf.Ticker(sym)
      hist = ticker.history(period="2d")
      previous_close_stock_price = hist.iloc[-2]['Close']
      current_stock_price = hist.iloc[-1]['Close']
      percent_change_stock_price = round((((current_stock_price - previous_close_stock_price) / previous_close_stock_price) * 100), 2)
      symbol_lookup_dict[sym] = {}
      symbol_lookup_dict[sym]['previous_close_stock_price'] = previous_close_stock_price
      symbol_lookup_dict[sym]['current_stock_price'] = current_stock_price
      symbol_lookup_dict[sym]['percent_change_stock_price'] = percent_change_stock_price
    except:
      print('------------------------')
      print(sym)
      print('did not work')
      print('------------------------')
      pass
  return symbol_lookup_dict