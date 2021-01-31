from flask import session
def set_session_variables_to_none_logout_function():
  session['logged_in_user_uuid'] = 'none'
  session['logged_in_user_email'] = 'none'
  session['logged_in_user_first_name'] = 'none'
  session['logged_in_user_last_name'] = 'none'
  session['logged_in_user_phone_number'] = 'none'