def invert_symbol_news_link_dict_function(input_arr_dict):
  """
  Return: invert the input array dict to a dict with user first
  """
  symbol_news_link_dict = {}
  for i in input_arr_dict:
    if i['symbol'] in symbol_news_link_dict:
      pass
    else:
      symbol_news_link_dict[i['symbol']] = i['google_news_link']
  return symbol_news_link_dict