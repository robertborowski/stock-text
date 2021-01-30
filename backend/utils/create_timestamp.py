from datetime import datetime
def create_timestamp_function():
  return datetime.now().strftime('%Y-%m-%d %H:%M:%S')