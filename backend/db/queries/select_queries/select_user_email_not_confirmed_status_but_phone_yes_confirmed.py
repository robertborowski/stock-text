import psycopg2
from psycopg2 import Error

def select_user_email_not_confirmed_status_but_phone_yes_confirmed_function(connection_postgres, cursor):
  """Returns: Pulls all users who do not have confirmed phone numbers"""
  try:
    # Run SQL
    cursor.execute("SELECT phone_number,email,first_name,uuid FROM login_information_table WHERE confirmed_phone_number=TRUE AND confirmed_email=FALSE AND delete_account_requested=FALSE")
    
    # Results from SQL query
    result_arr = cursor.fetchall()
    return result_arr

  # If Error when running the SQL  
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Error: ", error)
      confirm_status_email = None
      confirm_status_phone_number = None
      return confirm_status_email, confirm_status_phone_number