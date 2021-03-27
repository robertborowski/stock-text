def create_news_links_dict_function(input_arr):
  """
  Return: invert the input array dict to a dict with user first
  """
  # Set empty dict
  symbol_news_link_dict = {}
  
  # Loop through and add news link to every symbol
  for i in input_arr:
    if i[0] in symbol_news_link_dict:
      pass
    else:
      symbol_news_link_dict[i[0]] = i[1]
  
  # Return the dict
  return symbol_news_link_dict