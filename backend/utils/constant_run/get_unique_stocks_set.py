def get_unique_stocks_set_function(input_arr_dict):
  """Returns: Unique stocks in a set"""
  # Create empty unique stock set
  unique_stocks_set = set()
  
  # Loop and add only unique symbols to set
  for i in input_arr_dict:
    if i['symbol'] in unique_stocks_set:
      pass
    else:
      unique_stocks_set.add(i['symbol'])
  
  # Return the unique set
  return unique_stocks_set