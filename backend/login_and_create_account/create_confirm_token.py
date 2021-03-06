from flask import Flask, redirect, url_for, render_template, request, session, Blueprint
from itsdangerous import URLSafeTimedSerializer
import os

def create_confirm_token_function(user_field_to_verify, env_var_secret_key, env_var_secret_salt):
  """
  Returns: token for account confirmation link
  """
  serializer_instance = URLSafeTimedSerializer(env_var_secret_key)
  string_to_salt = env_var_secret_salt.encode("utf-8")
  token = serializer_instance.dumps(user_field_to_verify, salt=string_to_salt)
  return token