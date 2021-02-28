from flask import Flask, redirect, url_for, render_template, request, session, Blueprint, current_app
from itsdangerous import URLSafeTimedSerializer
import os
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.queries.update_queries.update_to_confirmed_email import update_to_confirmed_email_function

confirm_email_page = Blueprint("confirm_email_page", __name__, static_folder="static", template_folder="templates")
@confirm_email_page.route("/confirm/email/<confirm_email_token_url_variable>", methods=["POST", "GET"])
def confirm_email_page_function(confirm_email_token_url_variable):
  """
  Returns: confirms email token link
  """
  serializer_instance = URLSafeTimedSerializer(os.environ.get('URL_SAFE_SERIALIZER_SECRET_KEY_EMAIL'))
  string_to_salt = os.environ.get('URL_SAFE_SERIALIZER_SECRET_SALT_EMAIL').encode("utf-8")
  try:
    user_email_confirming = serializer_instance.loads(confirm_email_token_url_variable, salt=string_to_salt, max_age=3600)
    connection_postgres, cursor = connect_to_postgres_function()
    update_to_confirmed_email_function(connection_postgres, cursor, user_email_confirming)
  except:
    print('the token is expired!')
    return render_template('templates_user_logged_in/confirmed_email_page.html',
                          error_message_to_html = 'Verification link has expired.')
  return render_template('templates_user_logged_in/confirmed_email_page.html',
                          user_email_confirming_to_html = user_email_confirming)