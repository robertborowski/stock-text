def sanitize_name_input_create_account_function(name_not_sanitized):
  """
  Returns: Checks if the user inputs are valid/sanitized
  """
  name_not_sanitized = name_not_sanitized.lower()
  if (len(name_not_sanitized) < 2 or len(name_not_sanitized) > 20) or name_not_sanitized.isalpha() == False:
    return 'none'
  name_sanitized = name_not_sanitized
  return name_sanitized