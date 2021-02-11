def get_unique_stocks_set_function(input_arr_dict):
  """
  Returns: Unique stocks in a set
  """
  unique_stocks_set = set()
  for i in input_arr_dict:
    if i['symbol'] in unique_stocks_set:
      pass
    else:
      unique_stocks_set.add(i['symbol'])
  return unique_stocks_set