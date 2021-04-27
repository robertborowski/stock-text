import psycopg2
import psycopg2.extras
from psycopg2 import Error

def update_user_first_name_function(connection_postgres, cursor, user_first_name, user_uuid):
  """Returns: Updates the data in user database"""
  try:
    cursor.execute("UPDATE login_information_table SET first_name=%s WHERE uuid=%s AND delete_account_requested=FALSE", [user_first_name, user_uuid])
    connection_postgres.commit()
    print('Updated Information')
    #return 'Updated Information'
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Status: ", error)
      #return 'none'