import psycopg2
import psycopg2.extras
from psycopg2 import Error

def update_user_info_function(connection_postgres, cursor, user_email, user_first_name, user_last_name, user_phone_number, user_uuid):
  """
  Returns: Updates the data in user database
  """
  try:
    cursor.execute("UPDATE login_information_table SET email=%s, first_name=%s, last_name=%s, phone_number=%s WHERE uuid=%s AND delete_account_requested=FALSE", [user_email, user_first_name, user_last_name, user_phone_number, user_uuid])
    connection_postgres.commit()
    print('Updated Information')
    #return 'Updated Information'
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Status: ", error)
      #return 'none'