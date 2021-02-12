def create_queue_to_text_out_function(user_stocks_tracking_dict, user_phone_numbers_dict, symbol_percent_changes_dict, symbol_news_link_dict):
  """
  Loops through all the live data and creates a queue of people to text
  """
  queue_to_text_arr = []
  for k_user_uuid, v_symbols_dict in user_stocks_tracking_dict.items():
    for k_symbol, v_goal_percent in v_symbols_dict.items():
      current_percent_change = symbol_percent_changes_dict[k_symbol]['percent_change_stock_price']
      goal_percent_change = v_goal_percent
      if abs(current_percent_change) >= abs(goal_percent_change):
        if current_percent_change > 0:
          current_percent_change = '+' + str(current_percent_change)
        else:
          current_percent_change = str(current_percent_change)
        user_to_text_phone_number = user_phone_numbers_dict[k_user_uuid]
        google_link_to_text = symbol_news_link_dict[k_symbol]
        queue_to_text_arr.append((user_to_text_phone_number, k_symbol, current_percent_change, google_link_to_text))
  return queue_to_text_arr