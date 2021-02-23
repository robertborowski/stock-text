import psycopg2
from psycopg2 import Error
import os

def connect_to_postgres_function():
  """
  Returns: Postgres Connection and cursor
  """
  
  # Heroku Postgres connection
  DATABASE_URL = os.environ.get('DATABASE_URL')
  connection_postgres = psycopg2.connect(DATABASE_URL, sslmode='require')
  
  # Local Postgres connection
  """
  connection_postgres = psycopg2.connect(user = os.environ.get('POSTGRESQL_LOCAL_USER'),
                                        password = os.environ.get('POSTGRESQL_LOCAL_PASSWORD'),
                                        host = os.environ.get('POSTGRESQL_LOCAL_HOST'),
                                        port = os.environ.get('POSTGRESQL_LOCAL_PORT'),
                                        database = os.environ.get('POSTGRESQL_LOCAL_DATABASE_MARKET_TEXT') )
  """
  cursor = connection_postgres.cursor()
  return connection_postgres, cursor