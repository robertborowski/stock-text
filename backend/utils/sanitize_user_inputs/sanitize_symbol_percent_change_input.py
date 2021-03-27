def sanitize_symbol_percent_change_input_function(min_symbol_percent_change_not_sanitized):
  """
  Returns: Checks if the user inputs are valid/sanitized
  """
  min_symbol_percent_change_not_sanitized = float(min_symbol_percent_change_not_sanitized)
  
  if min_symbol_percent_change_not_sanitized >= 7 and min_symbol_percent_change_not_sanitized <= 99 and isinstance(min_symbol_percent_change_not_sanitized, float) == True:
    min_symbol_percent_change_sanitized = min_symbol_percent_change_not_sanitized
    return min_symbol_percent_change_sanitized
  else:
    return 'none'