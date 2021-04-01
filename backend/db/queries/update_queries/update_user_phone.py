import psycopg2
import psycopg2.extras
from psycopg2 import Error

def update_user_phone_function(connection_postgres, cursor, phone_input, user_uuid):
  """Returns: Updates the data in user database"""
  try:
    cursor.execute("UPDATE login_information_table SET phone_number=%s WHERE uuid=%s", [phone_input, user_uuid])
    connection_postgres.commit()
    print('Updated Information')
    #return 'Updated Information'
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Status: ", error)
      #return 'none'