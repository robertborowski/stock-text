from flask import Flask, redirect, url_for, render_template, request, session, Blueprint
from itsdangerous import URLSafeTimedSerializer
import os

def create_confirm_token_function(user_email):
  """
  Returns: token for account confirmation link
  """
  serializer_instance = URLSafeTimedSerializer(os.environ.get('URL_SAFE_SERIALIZER_SECRET_KEY'))
  string_to_salt = 'confirm-email'#.encode("utf-8")
  token = serializer_instance.dumps(user_email, salt=string_to_salt)
  session['confirm_email_token'] = token
  return token