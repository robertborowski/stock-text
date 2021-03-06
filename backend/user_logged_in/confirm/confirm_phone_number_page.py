from flask import Flask, redirect, url_for, render_template, request, session, Blueprint, current_app
from itsdangerous import URLSafeTimedSerializer
import os
from backend.db.connect_to_database import connect_to_postgres_function
from backend.db.queries.update_queries.update_to_confirmed_phone_number import update_to_confirmed_phone_number_function
from backend.db.close_connection_cursor_to_database import close_connection_cursor_to_database_function

confirm_phone_number_page = Blueprint("confirm_phone_number_page", __name__, static_folder="static", template_folder="templates")
@confirm_phone_number_page.route("/confirm/phone/<confirm_phone_number_token_url_variable>", methods=["POST", "GET"])
def confirm_phone_number_page_function(confirm_phone_number_token_url_variable):
  """Returns: confirms email token link"""
  serializer_instance = URLSafeTimedSerializer(os.environ.get('URL_SAFE_SERIALIZER_SECRET_KEY_PHONE'))
  string_to_salt = os.environ.get('URL_SAFE_SERIALIZER_SECRET_SALT_PHONE').encode("utf-8")
  try:
    user_phone_number_confirming = serializer_instance.loads(confirm_phone_number_token_url_variable, salt=string_to_salt, max_age=86400)
    connection_postgres, cursor = connect_to_postgres_function()
    update_to_confirmed_phone_number_function(connection_postgres, cursor, user_phone_number_confirming)
    close_connection_cursor_to_database_function(connection_postgres, cursor)
  except:
    # Set the session variables outgoing
    session['dashboard_upload_output_message'] = 'the phone number token has expired!'
    session['output_message_landing_page_session'] = 'the phone number token has expired!'
    
    # Redirect to page
    return redirect("https://symbolnews.com/dashboard", code=301)

  # Set the session variables outgoing
  session['dashboard_upload_output_message'] = 'Account phone number confirmed!'
  session['output_message_landing_page_session'] = 'Account phone number confirmed!'

  # Redirect to page
  return redirect("https://symbolnews.com/", code=301)