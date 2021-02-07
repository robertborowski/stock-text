def breakup_symbols_dict_from_ajax_function(dict):
  """
  Returns: Broken up symbols only from the ajax passed dictionary
  """
  symbols_arr = []
  for k, v in dict.items():
    for i in v:
      symbols_arr.append(i[0])
  return symbols_arr