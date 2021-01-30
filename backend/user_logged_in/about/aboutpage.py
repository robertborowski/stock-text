from flask import render_template, Blueprint, session
aboutpage = Blueprint("aboutpage", __name__, static_folder="static", template_folder="templates")
@aboutpage.route("/about", methods=["POST", "GET"])
def about_page_function():
	"""
	Returns: About page front end
	"""
	if session['logged_in_user_email'] != 'none':
		return render_template('templates_user_logged_in/about.html',
														user_email_from_session_to_html = session['logged_in_user_email'],
                            user_first_name_from_session_to_html = session['logged_in_user_first_name'],
                            user_last_name_from_session_to_html = session['logged_in_user_last_name'],
                            user_phone_number_from_session_to_html = session['logged_in_user_phone_number'])
	else:
		session['logged_in_user_uuid'] = 'none'
		session['logged_in_user_email'] = 'none'
		session['logged_in_user_first_name'] = 'none'
		session['logged_in_user_last_name'] = 'none'
		session['logged_in_user_phone_number'] = 'none'
		return render_template('templates_login_and_create_account/index.html')