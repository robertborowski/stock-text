import yfinance as yf

def yfinance_check_if_symbol_exists_function(input_symbol):
  """
  Returns: Checks if symbol exists or not
  """
  ticker = yf.Ticker(input_symbol)
  try:
    does_symbol_exist = ticker.info
  except:
    does_symbol_exist = 'none'
  finally:
    return does_symbol_exist