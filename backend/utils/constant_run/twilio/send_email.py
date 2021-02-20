import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email_function():
  message = Mail(
    from_email='from_email@example.com',
    to_emails='to_email@example.com',
    subject='Testing',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
  try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
    print('SUCCESS')
  except:
    print('FAILED')