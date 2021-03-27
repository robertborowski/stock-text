import psycopg2
from psycopg2 import Error

def insert_jobs_queues_table_function(connection_postgres, cursor, job_queue_name_input, stock_symbol):
  """Returns: inserts into database table when user submits stock to track"""

  postgres_insert_query = """INSERT INTO jobs_queues_table (job_queue_name, stored_item) VALUES (%s, %s)"""
  record_to_insert = (job_queue_name_input, stock_symbol)
  
  try:
    cursor.execute(postgres_insert_query, record_to_insert)
    connection_postgres.commit()
    output_message = 'Success!'
    return output_message
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Error: ", error)
      output_message = 'Insert not successful.'
      return output_message