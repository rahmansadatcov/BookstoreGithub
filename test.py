from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import abort
from flask import make_response
import sqlite3

app = Flask(__name__, static_url_path = "/images", static_folder = "images")

@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == "GET":
        con = sqlite3.connect('database.db')
        cur = con.cursor()

        cur.execute('SELECT isbn_13, title, cover FROM books')
        result = cur.fetchall()

        cur.close()
        con.close()

        return render_template('testing.html', page=url_for('welcome'))