import re

def sanitize_password_input_create_account_function(password_not_sanitized):
  """
  Returns: Checks if the user inputs are valid/sanitized
  """
  pattern = re.compile(r"(?=^.{8,20}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$")
  if pattern.match(password_not_sanitized):
    password_sanitized = password_not_sanitized
    return password_sanitized
  else:
    return 'none'