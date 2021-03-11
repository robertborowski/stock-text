from datetime import datetime
import os, time

def create_timestamp_function():
  """Returns: current datetime"""
  os.environ['TZ'] = 'US/Eastern'
  time.tzset()
  return datetime.now().strftime('%Y-%m-%d %H:%M:%S')