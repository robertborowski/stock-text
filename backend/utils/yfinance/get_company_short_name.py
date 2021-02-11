import yfinance as yf

def get_company_short_name_function(input_symbol):
  """
  Returns: Company short name from yfinance
  """
  ticker = yf.Ticker(input_symbol)
  company_short_name_without_spaces = ticker.info['shortName'].replace(" ", "_")
  return company_short_name_without_spaces
