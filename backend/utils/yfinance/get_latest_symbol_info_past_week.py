import yfinance as yf
from backend.utils.google_news.get_google_news_page import get_google_news_page_function

def get_latest_symbol_info_past_week_function(input_symbol):
  """
  Returns: Latest stock symbol information as dict
  """
  percent_change_stock_price = 0
  try:
    ticker = yf.Ticker(input_symbol)
    hist = ticker.history(period="5d")
    previous_close_stock_price = hist.iloc[-5]['Open']
    current_stock_price = hist.iloc[-1]['Close']
    percent_change_stock_price = round((((current_stock_price - previous_close_stock_price) / previous_close_stock_price) * 100), 2)
  except:
    print('------------------------')
    print(input_symbol)
    print('did not work/did not find symbol price')
    percent_change_stock_price = 0
    print('------------------------')
    pass

  percent_change_stock_price_to_str = str(percent_change_stock_price) + '%'

  if percent_change_stock_price > 0:
    percent_change_stock_price_to_str = '+' + percent_change_stock_price_to_str

  return percent_change_stock_price_to_str