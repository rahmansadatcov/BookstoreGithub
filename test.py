from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import abort

app = Flask(__name__)

@app.errorhandler(403)
def wrong_password(error):
    return render_template('wrong_passwd.html'), 403

@app.route('/')
def hello_world():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login(request.form['uname'], request.form['pwd'])
    else:
        return show_the_login_form()
    

def show_the_login_form():
    return render_template('login.html',page=url_for('login'))


def do_the_login(u,p):
    if (p == 'swordfish'):
        return f'<H1>Success!</H1>'
    else:
        abort(403)