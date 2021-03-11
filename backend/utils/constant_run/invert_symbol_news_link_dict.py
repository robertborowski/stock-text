def invert_symbol_news_link_dict_function(input_arr_dict):
  """
  Return: invert the input array dict to a dict with user first
  """
  # Set empty dict
  symbol_news_link_dict = {}
  
  # Loop through and add news link to every symbol
  for i in input_arr_dict:
    if i['symbol'] in symbol_news_link_dict:
      pass
    else:
      symbol_news_link_dict[i['symbol']] = i['google_news_link']
  
  # Return the dict
  return symbol_news_link_dict