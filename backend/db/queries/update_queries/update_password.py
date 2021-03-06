import psycopg2
import psycopg2.extras
from psycopg2 import Error

def update_password_function(connection_postgres, cursor, user_password, user_email):
  """
  Returns: Updates the data in user database
  """
  try:
    cursor.execute("UPDATE login_information_table SET password=%s WHERE email=%s AND delete_account_requested=FALSE", [user_password, user_email])
    connection_postgres.commit()
    print('Updated Information')
    #return 'Updated Information'
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Status: ", error)
      #return 'none'