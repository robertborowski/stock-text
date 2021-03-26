import re

def sanitize_symbol_input_function(symbol_not_sanitized):
  """
  Returns: Checks if the user inputs are valid/sanitized
  """
  symbol_not_sanitized = symbol_not_sanitized.upper()
  symbol_not_sanitized = symbol_not_sanitized.replace('.', '-')
  print('-----------------------------------')
  print('-------------------')
  print(symbol_not_sanitized)
  print('-------------------')
  print('-----------------------------------')

  pattern = re.compile("^[A-Z-]{1,6}$")
  if pattern.match(symbol_not_sanitized):
    symbol_sanitized = symbol_not_sanitized
    return symbol_sanitized
  else:
    return 'none'

  """
  if (len(symbol_not_sanitized) < 1 or len(symbol_not_sanitized) > 6): #or symbol_not_sanitized.isalpha() == False:
    for i in symbol_not_sanitized:

    return 'none'
  symbol_sanitized = symbol_not_sanitized
  return symbol_sanitized
  """