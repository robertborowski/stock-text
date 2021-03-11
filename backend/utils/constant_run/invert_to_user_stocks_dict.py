def invert_to_user_stocks_dict_function(input_arr_dict):
  """
  Return: invert the input array dict to a dict with user first
  """
  # Create empty dict
  user_stocks_tracking_dict = {}
  
  # Loop through make dict of uuid, symbol(s), percent threshold
  for i in input_arr_dict:
    user_stocks_tracking_dict[i['fk_user_uuid']] = {}
  for i in input_arr_dict:
    #user_stocks_tracking_dict[i['fk_user_uuid']][i['symbol']] = i['percent_change_to_notify']
    user_stocks_tracking_dict[i['fk_user_uuid']][i['symbol']] = {}
    user_stocks_tracking_dict[i['fk_user_uuid']][i['symbol']]['symbol_threshold'] = i['percent_change_to_notify']
    user_stocks_tracking_dict[i['fk_user_uuid']][i['symbol']]['pk_uuid_symbol_track'] = i['uuid']
  
  # Return the dict of user symbols with percent threshold
  return user_stocks_tracking_dict