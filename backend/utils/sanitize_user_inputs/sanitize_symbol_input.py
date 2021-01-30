def sanitize_symbol_input_function(symbol_not_sanitized):
  """
  Returns: Checks if the user inputs are valid/sanitized
  """
  symbol_not_sanitized = symbol_not_sanitized.upper()
  if (len(symbol_not_sanitized) < 1 or len(symbol_not_sanitized) > 5) or symbol_not_sanitized.isalpha() == False:
    return 'none'
  symbol_sanitized = symbol_not_sanitized
  return symbol_sanitized