def invert_to_user_phone_numbers_dict_function(input_arr_dict):
  """
  Return: invert the input array dict to a dict with user first
  """
  user_phone_numbers_dict = {}
  for i in input_arr_dict:
    user_phone_numbers_dict[i['uuid']] = i['phone_number']
  return user_phone_numbers_dict