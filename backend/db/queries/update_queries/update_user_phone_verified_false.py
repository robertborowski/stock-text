import psycopg2
import psycopg2.extras
from psycopg2 import Error

def update_user_phone_verified_false_function(connection_postgres, cursor, user_uuid):
  """Returns: Updates the data in user database"""
  try:
    cursor.execute("UPDATE login_information_table SET confirmed_phone_number=FALSE WHERE uuid=%s AND delete_account_requested=FALSE", [user_uuid])
    connection_postgres.commit()
    print('Updated Information')
    #return 'Updated Information'
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Status: ", error)
      #return 'none'