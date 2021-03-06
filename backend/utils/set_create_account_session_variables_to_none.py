from flask import session

def set_create_account_session_variables_to_none_function():
  """
  Returns: Sets all session variables to none
  """
  session['form_data_create_account_first_name'] = None
  session['form_data_create_account_last_name'] = None
  session['form_data_create_account_phone_number'] = None
  session['form_data_create_account_email'] = None
  session['form_data_create_account_password'] = None