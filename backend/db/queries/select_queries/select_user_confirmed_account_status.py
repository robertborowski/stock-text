import psycopg2
from psycopg2 import Error

def select_user_confirmed_account_status_function(connection_postgres, cursor, uuid_to_search):
  """
  Returns: Pulls all the symbols and percentages that the user is tracking
  """
  try:
    # Run SQL
    cursor.execute("SELECT confirmed_email,confirmed_phone_number FROM login_information_table WHERE uuid=%s", [uuid_to_search])
    
    # Results from SQL query
    result_row = cursor.fetchone()
    confirm_status_email = result_row[0]
    confirm_status_phone_number = result_row[1]
    
    # Email - Check if the results are False, if so assign new value
    if confirm_status_email == False:
      confirm_status_email = 'Email not confirmed! Check promotions/spam folders. SymbolNews will not send texts if email is not confirmed!'
    else:
      confirm_status_email = ''
    
    # Phone number - Check if the results are False, if so assign new value
    if confirm_status_phone_number == False:
      confirm_status_phone_number = 'Phone number not confirmed! Check for text message that contains the word "SymbolNews". SymbolNews will not send texts if phone number is not confirmed!'
    else:
      confirm_status_phone_number = ''
    return confirm_status_email, confirm_status_phone_number

  # If Error when running the SQL  
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Error: ", error)
      confirm_status_email = None
      confirm_status_phone_number = None
      return confirm_status_email, confirm_status_phone_number