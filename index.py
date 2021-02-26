# Imports
from flask import Flask, session
import os, time
from backend.login_and_create_account.loginpage import loginpage
from backend.login_and_create_account.create_account_render_page import create_account_render_page
from backend.login_and_create_account.creating_account_to_postgres import creating_account_to_postgres
from backend.login_and_create_account.login_attempt import login_attempt
from backend.user_logged_in.home.homepage import homepage
from backend.user_logged_in.about.aboutpage import aboutpage
from backend.user_logged_in.account.accountpage import accountpage
from backend.user_logged_in.logout.logout import logout
from backend.user_logged_in.home.upload_symbol_percent_change_input import upload_symbol_percent_change_input
from backend.user_logged_in.home.delete_symbols import delete_symbols
from backend.constant_run.background_run_main import pull_and_analyze_all_data_function
from backend.user_logged_in.account.accountpage_edit_information import accountpage_edit_information
from backend.user_logged_in.account.updating_account_info_postgres import updating_account_info_postgres
from backend.user_logged_in.account.delete_account_page import delete_account_page
from backend.user_logged_in.account.delete_account_perm import delete_account_perm
#==================================
from backend.user_logged_in.confirm.confirm_email_page import confirm_email_page
#==================================

# Set the timezone of the application when user creates account is will be in US/Easterm time
os.environ['TZ'] = 'US/Eastern'
time.tzset()
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
app.register_blueprint(delete_symbols, url_prefix="")
app.register_blueprint(accountpage_edit_information, url_prefix="")
app.register_blueprint(updating_account_info_postgres, url_prefix="")
app.register_blueprint(delete_account_page, url_prefix="")
app.register_blueprint(delete_account_perm, url_prefix="")
 #==================================
#session['confirm_email_token'] = 'temp'
#app.register_blueprint(confirm_email_page, url_prefix="")
#==================================

# Run the main program
if __name__ == "__main__":
  # Run local testing
  #app.run(debug = True)
  #app.run(debug = False)

  # port and run for Heroku
  port = int(os.environ.get('PORT', 5000))
  app.run(host = '0.0.0.0', port = port)