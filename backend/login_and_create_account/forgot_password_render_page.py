from flask import render_template, Blueprint

forgot_password_render_page = Blueprint("forgot_password_render_page", __name__, static_folder="static", template_folder="templates")
@forgot_password_render_page.route("/forgot_password")
def forgot_password_render_page_function():
  """
  Returns: Renders the create account page
  """
  return render_template('templates_login_and_create_account/forgot_password_page.html')