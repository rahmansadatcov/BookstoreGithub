from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import abort
from flask import make_response
import sqlite3

app = Flask(__name__)

@app.errorhandler(403)
def wrong_password(error):
    return render_template('wrong_passwd.html'), 403


@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == "GET":
        return show_welcome_page()
    elif request.method == "POST":
        if "login_btn" in request.form:
            return redirect(url_for('login'))
        elif "reg_btn" in request.form:
            return redirect(url_for('register'))

def show_welcome_page():
    return render_template('welcome.html', page=url_for("welcome"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return show_login_page()
    elif request.method == "POST":
        return do_the_login(request.form['uname'], request.form['pwd'])


def show_login_page():
    return render_template('login.html', page=url_for("login"))

def do_the_login(u, p):
    con = sqlite3.connect('database.db')
    cur = con.cursor();
    cur.execute("SELECT count(*) FROM admins WHERE name=? AND pwd=?;", (u, p))
    admin_found = (int(cur.fetchone()[0]))
    cur.close()
    con.close()
    if admin_found>0:
        return redirect(url_for('adminhome'))
    else:
        con = sqlite3.connect('database.db')
        cur = con.cursor();
        cur.execute("SELECT count(*) FROM users WHERE name=? AND pwd=?;", (u, p))
        user_found = (int(cur.fetchone()[0]))
        cur.close()
        con.close()
        if user_found>0:
            return f'<H1>You are in user page!</H1>'
        else:
            abort(403)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":    
        return show_register_page()
    elif request.method == "POST":
        return do_the_registration(request.form['uname'], request.form['pwd'])

def show_register_page():
    return render_template('register.html', page=url_for("register"))
    
    
def do_the_registration(u, p):
    con = sqlite3.connect('database.db')
    try:
        con.execute('CREATE TABLE users (name TEXT, pwd INT)')
    except:
        pass
    
    con.close()
    
    con = sqlite3.connect('database.db')
    con.execute("INSERT INTO users values(?,?);", (u, p))
    con.commit()
    con.close()
    
    return show_login_page()


@app.route('/adminhome', methods=['GET', 'POST'])
def adminhome():
    if request.method == 'GET':
        return show_admin_home_page()
    elif request.method == 'POST':
        return redirect(url_for('stocklevels'))
        

def show_admin_home_page():
    return render_template('adminhome.html', page=url_for("adminhome"))
    

@app.route('/stocklevels', methods=['GET', 'POST'])
def stocklevels():
    if request.method == 'GET':
        return show_stock_levels_page()
    elif request.method == 'POST':
        return redirect(url_for('addstock'))
    
def show_stock_levels_page():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    
    cur.execute('SELECT title, isbn_13, qty, cover FROM books')
    result = cur.fetchall()
    
    cur.close()
    con.close()
    
    return render_template('stocklevels.html', page=url_for("stocklevels"), variable=result)


@app.route('/addstock', methods=['GET', 'POST'])
def addstock():
    if request.method == 'GET':
        return show_add_stock_page()
    elif request.method == 'POST':
        if check_if_exists(request.form['isbn_13']) > 0:
            return update_stock(request.form['title'], request.form['author'], request.form['pub_date'], request.form['isbn_13'], request.form['retail'], request.form['trade'], request.form['qty'], request.form['cover'], request.form['description'])
        else:
            return add_to_stock(request.form['title'], request.form['author'], request.form['pub_date'], request.form['isbn_13'], request.form['retail'], request.form['trade'], request.form['qty'], request.form['cover'], request.form['description'])

def show_add_stock_page(): # make an addstock.html file
    return render_template('addstock.html', page=url_for('addstock'))
                            
def check_if_exists(i):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    
    cur.execute('SELECT EXISTS(SELECT 1 FROM books WHERE isbn_13 = (?))', (i, ))
    result = cur.fetchall()[0][0]

    cur.close()
    con.close()
    return result


def update_stock(ti, a, p, i, r, tr, q, c, d):
    con = sqlite3.connect('database.db')
    
    con.execute("UPDATE books SET title = (?), author = (?), pub_date = (?), retail_price = (?), trade_price = (?), qty = (?), cover = (?), description = (?) WHERE isbn_13 = (?)", (ti, a, p, r, tr, q, c, d, i))
    
    con.commit()
    con.close()
    
    return redirect(url_for('stocklevels'))
    


def add_to_stock(ti, a, p, i, r, tr, q, c, d):
    con = sqlite3.connect('database.db')

    con.execute("INSERT INTO books values(?,?,?,?,?,?,?,?,?);", (i, ti, a, p, r, tr, q, c, d))
    
    con.commit()
    con.close()        
    
    return redirect(url_for('stocklevels'))

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    