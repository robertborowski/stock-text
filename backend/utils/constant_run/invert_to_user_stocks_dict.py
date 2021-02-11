def invert_to_user_stocks_dict_function(input_arr_dict):
  """
  Return: invert the input array dict to a dict with user first
  """
  user_stocks_tracking_dict = {}
  for i in input_arr_dict:
    user_stocks_tracking_dict[i['fk_user_uuid']] = {}
  for i in input_arr_dict:
    user_stocks_tracking_dict[i['fk_user_uuid']][i['symbol']] = i['percent_change_to_notify']
  return user_stocks_tracking_dict