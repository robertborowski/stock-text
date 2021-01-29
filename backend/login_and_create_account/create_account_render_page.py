from flask import render_template, Blueprint
create_account_render_page = Blueprint("create_account_render_page", __name__, static_folder="static", template_folder="templates")
@create_account_render_page.route("/create_account")
def create_account_function():
  """
  Returns: Renders the create account page
  """
  return render_template('templates_login_and_create_account/create_account.html')