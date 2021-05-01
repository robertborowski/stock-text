import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

def send_email_weekly_recap_sym_thresholds_function(to_email_address_outgoing, weekly_sym_thresholds_value_dict, master_string):
  sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
  from_email = Email(email = "robert@symbolnews.com", name = "Symbol News")  # Change to your verified sender
  to_email = To(to_email_address_outgoing)  # Change to your recipient
  subject = "Symbol News - Weekly Recap"
  content = Content("text/plain", \
                    "Hi " + weekly_sym_thresholds_value_dict['first_name'] + ",\n\n" + \
                    "Total texts sent to you this week: " + str(weekly_sym_thresholds_value_dict['total_texts_this_week']) + \
                    "\n\nSummary this week:\n\n" + \
                    master_string +
                    "\n\nBest,\nRob from Symbol News")
  mail = Mail(from_email, to_email, subject, content)

  # Get a JSON-ready representation of the Mail object
  mail_json = mail.get()

  # Send an HTTP POST request to /mail/send
  #response = sg.client.mail.send.post(request_body=mail_json)
  sg.client.mail.send.post(request_body=mail_json)