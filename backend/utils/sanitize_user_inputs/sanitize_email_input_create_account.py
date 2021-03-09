import re

def sanitize_email_input_create_account_function(email_not_sanitized):
  """
  Returns: Checks if the user inputs are valid/sanitized
  """
  email_not_sanitized = email_not_sanitized.lower()
  pattern = re.compile("^[a-z0-9._-]{1,50}@[a-z0-9._-]{1,30}\.[a-z]{2,3}$")
  if pattern.match(email_not_sanitized):
    email_sanitized = email_not_sanitized
    return email_sanitized
  else:
    return 'none'