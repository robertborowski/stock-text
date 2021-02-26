from flask import Flask, redirect, url_for, render_template, request, session, Blueprint
from itsdangerous import URLSafeTimedSerializer
import os

confirm_email_page = Blueprint("confirm_email_page", __name__, static_folder="static", template_folder="templates")
@confirm_email_page.route("/confirm/email/<session['confirm_email_token']>", methods=["POST", "GET"])
def confirm_email_page_function():
  """
  Returns: confirms email token link
  """
  print('- - - - - - - - -')
  print(session['confirm_email_token'])
  print('- - - - - - - - -')

  serializer_instance = URLSafeTimedSerializer(os.environ.get('URL_SAFE_SERIALIZER_SECRET_KEY'))#.encode("utf-8"))
  string_to_salt = "confirmemail".encode("utf-8")
  try:
    user_email_confirming = serializer_instance.loads(session['confirm_email_token'], salt=string_to_salt, max_age=3600)
  except:
    print('the token is expired!')
    return '<h1>the token is expired!</h1>'
  return render_template('templates_user_logged_in/confirmed_email_page.html',
                          user_email_confirming_to_html = user_email_confirming)