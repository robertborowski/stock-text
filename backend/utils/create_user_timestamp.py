from datetime import datetime
def create_user_timestamp_function():
  return datetime.now().strftime('%Y-%m-%d %H:%M:%S')