import re

def sanitize_email_input_create_account_function(email_not_sanitized):
  """
  Returns: Checks if the user inputs are valid/sanitized
  """
  pattern = re.compile("^[A-Za-z0-9._-]{1,50}@[A-Za-z0-9._-]{1,30}\.[A-Za-z]{2,3}$")
  if pattern.match(email_not_sanitized):
    email_sanitized = email_not_sanitized
    return email_sanitized
  else:
    return 'none'