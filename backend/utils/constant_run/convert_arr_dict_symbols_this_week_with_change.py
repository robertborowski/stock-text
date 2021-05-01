from backend.utils.yfinance.get_latest_symbol_info_past_week import get_latest_symbol_info_past_week_function

def convert_arr_dict_symbols_this_week_with_change_function(input_arr):
  """Return: convert array to nested dict for users who received texts this week"""
  dict = {}

  for i in input_arr:
    if i not in dict:
      dict[i] = get_latest_symbol_info_past_week_function(i)

  return dict