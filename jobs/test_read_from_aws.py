import pandas as pd
import boto3
import os

def run():
  try:
    bucket = os.environ.get('AWS_SYMBOLNEWS_BUCKET_NAME')
    file_name = "2021-04-28 verify_email_reminders_sent_table.csv"

    s3 = boto3.client('s3') 
    obj = s3.get_object(Bucket= bucket, Key= file_name) 

    initial_df = pd.read_csv(obj['Body']) # 'Body' is a key word
    print(initial_df)
  except:
    'did not find file in AWS s3'

# Run the main program
if __name__ == "__main__":
  run()