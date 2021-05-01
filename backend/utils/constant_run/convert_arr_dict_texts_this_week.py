def convert_arr_dict_texts_this_week_function(input_arr, sym_week_threshold_dict):
  """Return: convert array to nested dict for users who received texts this week"""    
  dict = {}

  for i in input_arr:
    # If email not in dict
    if i[1] not in dict:
      dict[i[1]] = {}
      dict[i[1]]['uuid'] = i[5]
      dict[i[1]]['first_name'] = i[2]
      dict[i[1]]['total_texts_this_week'] = 1
      dict[i[1]]['symbols'] = {}
      dict[i[1]]['symbols'][i[3]] = {}
      dict[i[1]]['symbols'][i[3]]['total_percent_change_this_week'] = sym_week_threshold_dict[i[3]]
      dict[i[1]]['symbols'][i[3]]['google_news_link'] = i[4]
    
    # If email already in dict, add the additional symbols to nested dict
    else:
      if i[3] not in dict[i[1]]['symbols']:
        dict[i[1]]['total_texts_this_week'] += 1
        dict[i[1]]['symbols'][i[3]] = {}
        dict[i[1]]['symbols'][i[3]]['total_percent_change_this_week'] = sym_week_threshold_dict[i[3]]
        dict[i[1]]['symbols'][i[3]]['google_news_link'] = i[4]

  return dict