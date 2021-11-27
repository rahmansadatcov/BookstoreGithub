from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import abort
from flask import make_response
from flask import flash
from flask import session
from werkzeug.utils import secure_filename
from markupsafe import escape
import sqlite3
import os


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


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
            return redirect(url_for('userhome'))
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
    return render_template('stocklevels.html', page=url_for("stocklevels"), all_books=result)


@app.route('/addstock', methods=['GET', 'POST'])
def addstock():
    if request.method == 'GET':
        return show_add_stock_page()
    elif request.method == 'POST':
        # For some reason the code below gets me a 400 error
#         image = request.files['image']
        
        image_path = "/home/codio/workspace/cover_images/" + request.form["cover"]
        
        if check_if_exists(request.form['isbn_13']) > 0:
            return update_stock(request.form['title'], request.form['author'], request.form['pub_date'], request.form['isbn_13'], request.form['retail'], request.form['trade'], request.form['qty'], image_path, request.form['description'])
        else:
            return add_to_stock(request.form['title'], request.form['author'], request.form['pub_date'], request.form['isbn_13'], request.form['retail'], request.form['trade'], request.form['qty'], image_path, request.form['description'])

def show_add_stock_page():
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
    
    save_image()
    
    con = sqlite3.connect('database.db')

    con.execute("INSERT INTO books values(?,?,?,?,?,?,?,?,?);", (i, ti, a, p, r, tr, q, c, d))
    
    con.commit()
    con.close()        
    
    return redirect(url_for('stocklevels'))


@app.route('/home', methods=['GET'])
def userhome():
    if request.method == 'GET':
        return show_user_home_page()
#     if request.method == 'POST':
#         pass
            

def show_user_home_page():
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    cur.execute('SELECT isbn_13, title, cover, retail_price FROM books')
    result = cur.fetchall()

    cur.close()
    con.close()

    return render_template('userhome.html', page=url_for('userhome'), all_books=result)


@app.route('/addtocart', methods=['POST'])
def add_to_cart():
#     try:
    if request.method == 'POST':
        
        
        con = sqlite3.connect('database.db')
        cur = con.cursor()

        cur.execute('SELECT isbn_13, title, retail_price, cover, qty FROM books WHERE isbn_13=(?);', (request.form["isbn_13"], ))
        book = cur.fetchone()
        bookArray = dict()
        
        bookArray = {book[0]: {"cover": book[3], "isbn_13": book[0], "retail_price": book[2], "occurence": 1, "qty": book[4], "title": book[1]}}
        
        isbn = book[0]
        price = book[2]
        
        total_price = 0
        total_quantity = 0
        
        session.modified = True
        
        if 'cart_book' in session:
            print('cart_book in session')
            if isbn in session['cart_book']:
                print('same item in session')
                session['cart_book'][isbn]['occurence'] = session['cart_book'][isbn]['occurence'] + 1
            else:
                print('no same item in session')
                session['cart_book'] = array_merge(session['cart_book'], bookArray)
        
            for key, value in session['cart_book'].items():
                print('looping through the session to find the total price and quantity')
                individual_quantity = session['cart_book'][key]['occurence']
                individual_price = session['cart_book'][key]['retail_price']
                total_quantity = total_quantity + individual_quantity
                total_price = total_price + individual_price * individual_quantity
            
        else:
            print('cart_book NOT in session')


            session['cart_book'] = bookArray
            total_price = total_price + price
            total_quantity = total_quantity + 1

        session['total_quantity'] = round(total_quantity, 2)
        session['total_price'] = round(total_price, 2)
        
                                                                                             
        cur.close()
        con.close()
                                                                                                  
        return redirect(url_for('userhome'))
        
def array_merge( first_array , second_array ):
	if isinstance( first_array , list ) and isinstance( second_array , list ):
		return first_array + second_array
	elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
		return dict( list( first_array.items() ) + list( second_array.items() ) )
	elif isinstance( first_array , set ) and isinstance( second_array , set ):
		return first_array.union( second_array )
	return False		        


@app.route('/shoppingcart', methods=['POST'])
def shopping_cart():
    if request.method == 'POST':
        return show_shopping_cart()

def show_shopping_cart(): 
    return render_template('shoppingcart.html', page=url_for('shopping_cart'))

@app.route('/emptycart', methods=['POST'])
def empty_cart():
    if request.method == 'POST':        
        session.clear()
        return redirect(url_for('userhome'))

@app.route('/gobackhome', methods=['POST'])
def go_back_home():
    if request.method == 'POST':
        return show_user_home_page()

@app.route('/deletebook', methods=['POST'])
def deletebook():
    print('WORKS 1')
    if request.method == 'POST':
        print('WORKS 2')
        isbn = request.form.get('isbn_13')
        print('WORKS 3')
        print('This is the isbn:', isbn)
        if isbn in session['cart_book']:
            print('WORKS 4')
            if len(session['cart_book'].keys()) > 1:
                session['total_quantity'] = session['total_quantity'] - session['cart_book'][isbn]['occurence']
                session['total_price'] = round(session['total_price'] - session['total_quantity'] * session['cart_book'][isbn]['retail_price'], 2)
                del session['cart_book'][isbn]
                print('item removed')
                return show_shopping_cart()
            else:
                session.clear()
                print('whole ')
                return show_user_home_page()
        print('WORKS 5')

        
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    