import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
from backend.utils.create_uuid import create_uuid_function
from backend.utils.create_timestamp import create_timestamp_function
from backend.db.queries.insert_queries.insert_sent_recap_email_table import insert_sent_recap_email_table_function

def send_email_weekly_recap_sym_thresholds_function(to_email_address_outgoing, weekly_sym_thresholds_value_dict, master_string, email_send_date, connection_postgres, cursor, symbols_sent_arr):
  sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
  from_email = Email(email = "robert@symbolnews.com", name = "Symbol News")  # Change to your verified sender
  to_email = To(to_email_address_outgoing)  # Change to your recipient
  subject = "Weekly Recap - " + email_send_date
  content = Content("text/plain", \
                    "Hi " + weekly_sym_thresholds_value_dict['first_name'] + ",\n\n" + \
                    "Total texts sent to you this week: " + str(weekly_sym_thresholds_value_dict['total_texts_this_week']) + \
                    "\n\nSummary this week (% price change from Monday open to Friday close):\n\n" + \
                    master_string +
                    "\n\nBest,\nRob from Symbol News")
  mail = Mail(from_email, to_email, subject, content)

  # Get a JSON-ready representation of the Mail object
  mail_json = mail.get()

  # Send an HTTP POST request to /mail/send
  #response = sg.client.mail.send.post(request_body=mail_json)
  sg.client.mail.send.post(request_body=mail_json)

  # After email sent, insert tracking row into database
  user_uuid = weekly_sym_thresholds_value_dict['uuid']

  # Add the UUID and timestamp for datetime that the account was created
  user_uuid_sent_email_recap = create_uuid_function("snde_")
  user_sent_email_recap_timestamp = create_timestamp_function()

  insert_email_recap_status = insert_sent_recap_email_table_function(connection_postgres, cursor, user_uuid_sent_email_recap, user_sent_email_recap_timestamp, user_uuid, mail_json, weekly_sym_thresholds_value_dict['total_texts_this_week'], symbols_sent_arr)
  print(insert_email_recap_status)