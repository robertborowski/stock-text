from flask import Flask, redirect, url_for, render_template, request, session, Blueprint
from itsdangerous import URLSafeTimedSerializer
import os
#==================================
from backend.user_logged_in.confirm.confirm_email_page import confirm_email_page
#==================================

def create_confirm_token_function(user_email):
  """
  Returns: token for account confirmation link
  """
  serializer_instance = URLSafeTimedSerializer(os.environ.get('URL_SAFE_SERIALIZER_SECRET_KEY'))
  string_to_salt = 'confirmemail'.encode("utf-8")
  token = serializer_instance.dumps(user_email, salt=string_to_salt)
  session['confirm_email_token'] = token
  #==================================
  # Flask constructor
  app = Flask(__name__)
  # To use a session, there has to be a secret key. The string should be something difficult to guess
  app.secret_key = os.urandom(64)
  app.register_blueprint(confirm_email_page, url_prefix="")
  #==================================
  return token