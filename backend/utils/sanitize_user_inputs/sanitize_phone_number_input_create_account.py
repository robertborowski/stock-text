def sanitize_phone_number_input_create_account_function(phone_number_not_sanitized):
  """
  Returns: Checks if the user inputs are valid/sanitized
  """
  if len(phone_number_not_sanitized) != 10 or phone_number_not_sanitized.isdigit() == False:
    return 'none'
  phone_number_sanitized = phone_number_not_sanitized
  return phone_number_sanitized