# Imports
from flask import Flask
import os
from backend.login_and_create_account.loginpage import loginpage
from backend.login_and_create_account.create_account_render_page import create_account_render_page
from backend.login_and_create_account.creating_account_to_postgres import creating_account_to_postgres
from backend.login_and_create_account.login_attempt import login_attempt
from backend.user_logged_in.home.homepage import homepage
from backend.user_logged_in.about.aboutpage import aboutpage
from backend.user_logged_in.account.accountpage import accountpage
from backend.user_logged_in.logout.logout import logout
from backend.user_logged_in.home.upload_symbol_percent_change_input import upload_symbol_percent_change_input
from backend.user_logged_in.home.home_see_symbol_list_page import home_see_symbol_list_page
# Flask constructor
app = Flask(__name__)
# To use a session, there has to be a secret key. The string should be something difficult to guess
app.secret_key = os.urandom(64)
# Blue prints to run python script from multiple files
app.register_blueprint(loginpage, url_prefix="")
app.register_blueprint(create_account_render_page, url_prefix="")
app.register_blueprint(creating_account_to_postgres, url_prefix="")
app.register_blueprint(login_attempt, url_prefix="")
app.register_blueprint(homepage, url_prefix="")
app.register_blueprint(aboutpage, url_prefix="")
app.register_blueprint(accountpage, url_prefix="")
app.register_blueprint(logout, url_prefix="")
app.register_blueprint(upload_symbol_percent_change_input, url_prefix="")
app.register_blueprint(home_see_symbol_list_page, url_prefix="")
# Run the main program
if __name__ == "__main__":
  app.run(debug = True)