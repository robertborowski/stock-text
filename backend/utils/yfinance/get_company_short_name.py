import yfinance as yf

def get_company_short_name_function(input_symbol):
  """
  Returns: Company short name from yfinance
  """
  ticker = yf.Ticker(input_symbol)
  try:
    print('company shortname: ' + str(ticker.info['shortName']))
  except:
    print('yfinance cannot find company short name')

  try:
    company_short_name_without_spaces = ticker.info['shortName'].replace(" ", "_")
  except:
    company_short_name_without_spaces = str(input_symbol) + '_stock'
  return company_short_name_without_spaces