import psycopg2
from psycopg2 import Error

def delete_job_company_short_name_function(connection_postgres, cursor, job_name, symbol):
  """Returns: deletes from jobs table in database"""
  postgres_delete_symbols_query = """DELETE FROM jobs_queues_table WHERE job_queue_name=%s AND stored_item=%s;"""
  record_to_delete = (job_name, symbol)
  try:
    cursor.execute(postgres_delete_symbols_query, record_to_delete)
    connection_postgres.commit()
    print('Status: row deleted from table')
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Status: ", error)
  return True