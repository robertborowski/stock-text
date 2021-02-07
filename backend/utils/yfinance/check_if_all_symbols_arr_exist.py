from backend.utils.yfinance.yfinance_check_if_symbol_exists import yfinance_check_if_symbol_exists_function

def check_if_all_symbols_arr_exist_function(input_arr):
  """
  Returns: True if all symbols exist, none if any of the input symbols do not exist
  """
  for sym in input_arr:
    does_symbol_exist = yfinance_check_if_symbol_exists_function(sym)
    if does_symbol_exist == 'none':
      return 'none'
  return True