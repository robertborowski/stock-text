import os
import datetime
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function
from backend.utils.create_timestamp import create_timestamp_function
from backend.db.queries.select_queries.select_all_database_table_names import select_all_database_table_names_function
import logging
import boto3
from botocore.exceptions import ClientError
import io
from io import StringIO
import psycopg2
import pandas as pd

def job_remind_verify_phone_function():
  """Return: Go into all database tables, pull table info as separate csv files, store all csv's in s3 bucket for that day"""
  # Schedule for only certain days of the week
  """num_day_of_week = datetime.datetime.today().weekday()
  if num_day_of_week == 0 or num_day_of_week == 1 or num_day_of_week == 2 or num_day_of_week == 3 or num_day_of_week == 4 or num_day_of_week == 5:
    return True"""

  # Create AWS s3 client
  s3_resource = boto3.resource('s3')
  s3_bucket_name = os.environ.get('AWS_SYMBOLNEWS_BUCKET_NAME')
  
  # Connect to database
  connection_postgres, cursor = connect_to_postgres_function()

  # Get all table names in the current database
  db_table_names_arr = select_all_database_table_names_function(connection_postgres, cursor)

  for i in db_table_names_arr:
    # Get table name
    table_name = i[0]
    try:
      # Run sql statement on the table and get all row results
      cursor.execute("SELECT * FROM %s" % table_name)
      result_list = cursor.fetchall()
      
      # Get table headers, store in array
      headers_tuple = cursor.description
      headers_arr = []
      for i in headers_tuple:
        headers_arr.append(i.name)
      
      # Create into pandas dataframe
      df = pd.DataFrame(result_list, columns=headers_arr)

      # Get todays date as string
      todays_date_str = str(datetime.datetime.now().date())
      todays_date = todays_date_str.replace("-","")

      # Upload pandas df into aws s3
      csv_buffer = StringIO()
      df.to_csv(csv_buffer)
      s3_resource.Object(s3_bucket_name, todays_date + ' ' + table_name + '.csv').put(Body=csv_buffer.getvalue())
    
    except (Exception, psycopg2.Error) as error:
      if(connection_postgres):
        print("Error: ", error)
        result_list = 'none'
        return result_list

  # Close connection
  close_connection_cursor_to_database_function(connection_postgres, cursor)

# Run the main program
if __name__ == "__main__":
  print('= = = = = = = = = = = = = = = = = JOB START (job_remind_verify_phone_function) = = = = = = = = = = = = = = = = =')
  job_remind_verify_phone_function()
  print('= = = = = = = = = = = = = = = = = JOB END (job_remind_verify_phone_function) = = = = = = = = = = = = = = = = =')