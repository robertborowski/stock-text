import psycopg2
import psycopg2.extras
from psycopg2 import Error

def update_to_confirmed_phone_number_function(connection_postgres, cursor, user_phone_number):
  """
  Returns: Updates the data in user database
  """
  try:
    cursor.execute("UPDATE login_information_table SET confirmed_phone_number=TRUE WHERE phone_number=%s", [user_phone_number])
    connection_postgres.commit()
    print('Updated Information')
    #return 'Updated Information'
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Status: ", error)
      #return 'none'