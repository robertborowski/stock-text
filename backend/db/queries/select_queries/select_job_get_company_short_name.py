import psycopg2
from psycopg2 import Error

def select_job_get_company_short_name_function(connection_postgres, cursor, job_name_to_search):
  """Returns: Pulls all the symbols and percentages that the user is tracking"""
  try:
    cursor.execute("SELECT stored_item FROM jobs_queues_table WHERE job_queue_name=%s", [job_name_to_search])
    result_list = cursor.fetchall()
    return result_list
  except (Exception, psycopg2.Error) as error:
    if(connection_postgres):
      print("Error: ", error)
      result_list = 'none'
      return result_list