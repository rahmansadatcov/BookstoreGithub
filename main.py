from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import abort
from flask import make_response
from flask import flash
from flask import session
from markupsafe import escape
from werkzeug.utils import secure_filename
import sqlite3
import os

# Initiating our Flask app.
app = Flask(__name__)

# Configuring the upload folder (where the cover images uploaded from the admin will be saved)
UPLOAD_FOLDER = '/cover_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Setting a secret key that is difficult to guess.
app.secret_key = b'_5#y2L"24K8.\n\xec]/'


@app.errorhandler(403)
# The function below catches the 403 error and lets the user know they have inputted a wrong user/pass combination.
def wrong_password(error):
    return render_template('wrong_passwd.html'), 403


@app.route('/', methods=['GET', 'POST'])
# The function below handles the GET and POST requests for the welcome page.
def welcome():
    # If we get a GET request, we display the welcome page.
    if request.method == "GET": 
        return show_welcome_page()
    # If we get a POST request, we either redirect to the login page or the register page, depending on which button was pressed.
    elif request.method == "POST":
        if "login_btn" in request.form:
            return redirect(url_for('login'))
        elif "reg_btn" in request.form:
            return redirect(url_for('register'))

# The function below displays the welcome page.
def show_welcome_page():
    return render_template('welcome.html', page=url_for("welcome"))


@app.route('/login', methods=['GET', 'POST'])
# The function below handles the GET and POST requests for the login page.
def login():
    # If we get a GET request, we display the login page.
    if request.method == "GET":
        return show_login_page()
    # If we get a POST request, we use the values the user inputted to perform the login.
    elif request.method == "POST":
        return do_the_login(request.form['uname'], request.form['pwd'])

# The function below displays the login page.
def show_login_page():
    return render_template('login.html', page=url_for("login"))

# The function below performs the login.
def do_the_login(u, p):
    
    
    con = sqlite3.connect('database.db')
    cur = con.cursor();
    
    # We look for a record in the 'admins' table in our database that satisfies the username/password combination the user inputted.
    cur.execute("SELECT count(*) FROM admins WHERE name=? AND pwd=?;", (u, p)) # The sql function 'count()' will return how many such records exist.
    admin_found = (int(cur.fetchone()[0])) # We store that number in 'admin_found'.
    
    cur.close()
    con.close()
    
    # If there is a record that satisfies the username/password combination , we display the admin home page.
    if admin_found>0:
        return redirect(url_for('adminhome'))
    # If not, then we do the same process for the 'users' table.
    else:
        con = sqlite3.connect('database.db')
        cur = con.cursor();
        
        # We look for a record in the 'users' table in our database that satisfies the username/password combination the user inputted.
        cur.execute("SELECT count(*) FROM users WHERE name=? AND pwd=?;", (u, p)) # The sql function 'count()' will return how many such records exist.
        user_found = (int(cur.fetchone()[0])) # We store that number in 'user_found'.
        
        cur.close()
        con.close()
        # If there is a record that satisfies the username/password combination , we display the user home page.
        if user_found>0:
            return redirect(url_for('userhome'))
        # If not, then we throw an error to let the user know they have inputted a wrong user/pass combination.
        else:
            abort(403)


@app.route('/register', methods=['GET', 'POST'])
# The function below handles the GET and POST requests for the register page.
def register():
    # If we get a GET request, we display the register page.
    if request.method == "GET":    
        return show_register_page()
    # If we get a POST request, we use the values the user inputted to perform the registration.
    elif request.method == "POST":
        return do_the_registration(request.form['uname'], request.form['pwd'])

# The function below displays the register page.
def show_register_page():
    return render_template('register.html', page=url_for("register"))
    
# The function below performs the registration.
def do_the_registration(u, p):
    con = sqlite3.connect('database.db')
    
    # The code below tries to create a 'users' table, if one hasn't been created already.
    try:
        con.execute('CREATE TABLE users (name TEXT, pwd INT)')
    except:
        pass
    
    con.close()
    
    con = sqlite3.connect('database.db')
    
    # We insert the username/password combination that the user inputted into the 'users' table
    con.execute("INSERT INTO users values(?,?);", (u, p))
    
    con.commit()
    con.close()
    
    # We redirect to the login page.
    return show_login_page()


@app.route('/adminhome', methods=['GET', 'POST'])
# The function below handles the GET and POST requests for the admin home page.
def adminhome():
    # If we get a GET request, we display the admin home page.
    if request.method == 'GET':
        return show_admin_home_page()
    # If we get a POST request, we redirect to the stock levels page.
    elif request.method == 'POST':
        return redirect(url_for('stocklevels'))
        
# The function below displays the admin home page.
def show_admin_home_page():
    return render_template('adminhome.html', page=url_for("adminhome"))
    

@app.route('/stocklevels', methods=['GET', 'POST'])
# The function below handles the GET and POST requests for the stock levels page.
def stocklevels():
    # If we get a GET request, we display the stock levels page.
    if request.method == 'GET':
        return show_stock_levels_page()
    # If we get a POST request, we redirect to the add stock page.
    elif request.method == 'POST':
        return redirect(url_for('addstock'))

# The function below displays the stock levels page.
def show_stock_levels_page():
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    # We select the attributes we want from all the records from the 'books' table in our database.
    cur.execute('SELECT title, isbn_13, qty, cover FROM books')
    result = cur.fetchall() # We store our findings in 'result'.
    
    cur.close()
    con.close()
    return render_template('stocklevels.html', page=url_for("stocklevels"), all_books=result)


@app.route('/addstock', methods=['GET', 'POST'])
# The function below handles the GET and POST requests for the add stock page.
def addstock():
    # If we get a GET request, we display the add stock page.
    if request.method == 'GET':
        return show_add_stock_page()
    # If we get a POST request, we use the values the user inputted to add a record in the 'books' table in our database.
    elif request.method == 'POST':
        
        # We save the image inputted by the user to our file system (specifically in the /static/cover_images folder)
        # The next 2 lines do not work (I've tried MANY code variations, but the file always gets saved in the main directory of the project instead of being saved in '/static/cover_images')
        image = request.files['image']
        image.save(image.filename)
     
        # We request the file name of the image the user inputted and use it to then set 'image_path' as the path to that file.
        image_path = "cover_images/" + image.filename
        
        # If a record with the same isbn exists, we use the values the user inputted to update the existing record in our database.
        if check_if_exists(request.form['isbn_13']) > 0:
            return update_stock(request.form['title'], request.form['author'], request.form['pub_date'], request.form['isbn_13'], request.form['retail'], request.form['trade'], request.form['qty'], image_path, request.form['description'])
        # If not, then we use the values the user inputted to create a new record in our database.
        else:
            return add_to_stock(request.form['title'], request.form['author'], request.form['pub_date'], request.form['isbn_13'], request.form['retail'], request.form['trade'], request.form['qty'], image_path, request.form['description'])

# The function below displays the add stock page.
def show_add_stock_page():
    return render_template('addstock.html', page=url_for('addstock'))


# The function below checks whether a record exists in the 'books' table in our database.
def check_if_exists(i):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    
    # We check if there is a record in the 'books' table that has the same isbn_13 value (primary key) as the one that was passed in this function.
    cur.execute('SELECT EXISTS(SELECT 1 FROM books WHERE isbn_13 = (?))', (i, )) # The sql operation 'EXISTS' will return a boolean value based on whether such a record exists or not.
    result = cur.fetchall()[0][0] # We store that number in 'result'.

    cur.close()
    con.close()
    return result

# The function below updates an existing record in the 'books' table in our database.
def update_stock(ti, a, p, i, r, tr, q, c, d):
    
    con = sqlite3.connect('database.db')
    
    # We update a record in the database by setting each and every one of its attributes to the corresponding value, based on what the user inputted.
    con.execute("UPDATE books SET title = (?), author = (?), pub_date = (?), retail_price = (?), trade_price = (?), qty = (?), cover = (?), description = (?) WHERE isbn_13 = (?)", (ti, a, p, r, tr, q, c, d, i))
    
    con.commit()
    con.close()
    
    # We redirect back to the stock levels page.
    return redirect(url_for('stocklevels'))

# The function below creates a new record in the 'books' table in our database.
def add_to_stock(ti, a, p, i, r, tr, q, c, d):

    con = sqlite3.connect('database.db')
    
    # We add a new record in the database by specifying each and every one of its attributes, based on what the user inputted.
    con.execute("INSERT INTO books values(?,?,?,?,?,?,?,?,?);", (i, ti, a, p, r, tr, q, c, d))

    con.commit()
    con.close()        

    # We redirect back to the stock levels page.
    return redirect(url_for('stocklevels'))


@app.route('/home', methods=['GET'])
# The function below handles the GET request for the user home page.
def userhome():
    # If we get a GET request, we display the user home page.
    if request.method == 'GET':
        return show_user_home_page()
            
# The function below displays the user home page.
def show_user_home_page():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    
    # We select the attributes we want from all the records from the 'books' table in our database.
    cur.execute('SELECT isbn_13, title, cover, retail_price FROM books')
    result = cur.fetchall() # We store our findings in 'result'.

    cur.close()
    con.close()

    return render_template('userhome.html', page=url_for('userhome'), all_books=result)


@app.route('/addtocart', methods=['POST'])
# The function below handles the POST request for the add to cart page.
def add_to_cart():
    # If we get a POST request, we add the book selected to the cart.
    if request.method == 'POST':
        
        
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        
        # We select the attributes we want from the record that has the same isbn value as the one found in the hidden input of the form submitted on the html page.
        cur.execute('SELECT isbn_13, title, retail_price, cover, qty FROM books WHERE isbn_13=(?);', (request.form["isbn_13"], ))
        book = cur.fetchone() # We store our findings in 'book'.
        
        
        # We create a dictionary that has: a) the isbn of the book as key and b) a dictionary of all the attributes as value.
        # This dictionary will essentially serve as a container for all the information about the current book being added to the shopping cart.
        bookArray = dict()
        bookArray = {book[0]: {"cover": book[3], "isbn_13": book[0], "retail_price": book[2], "occurence": 1, "qty": book[4], "title": book[1]}}
        
        # We set these variables as the isbn and the retail price of the book currently being added to the cart (the reason we do this is for ease of use).
        isbn = book[0]
        price = book[2]
        
        # We declare two variables 'total_price' and 'total_quantity' and we initially set them as 0.
        total_price = 0
        total_quantity = 0
        
        # We set this flag as True to declare that modifications are going to be made to Flask's session.
        session.modified = True
        
        # Note: In the lines 299-330 there are a lot of print statements that I did not remove, to showcase how I debugged my code whenever I was facing problems.
        
        # We check if there is already a book in the cart.
        if 'cart_book' in session:
            print('cart_book in session')
            # If yes, we check if the same book exists in the cart already.
            if isbn in session['cart_book']:
                print('same item in session')
                # If yes, we simply increase the value of the 'occurence' key by 1.
                session['cart_book'][isbn]['occurence'] = session['cart_book'][isbn]['occurence'] + 1
            else:
                print('no same item in session')
                # If not, then we use the 'array_merge' function to merge the current book with the ones that are already in the session and we store the result in the session again.
                session['cart_book'] = array_merge(session['cart_book'], bookArray)
            
            # Here we loop through each book and add up all the occurences and the prices so we can have the totals stored in 'total_quantity' and 'total_price'.
            for key, value in session['cart_book'].items():
                print('looping through the session to find the total price and quantity')
                unit_quantity = session['cart_book'][key]['occurence']
                unit_price = session['cart_book'][key]['retail_price']
                total_quantity = total_quantity + unit_quantity
                total_price = total_price + unit_price * unit_quantity
        else:
            print('cart_book NOT in session')
            # If not, then we add the current book (bookArray) in the session as a value of the key 'cart_book'.
            # We also increment the 'total_price' and the 'total_quantity' accordingly.
            session['cart_book'] = bookArray
            total_price = total_price + price
            total_quantity = total_quantity + 1
        
        # We store 'total_quantity' and 'total_price' in the session so we can use it when needed.
        session['total_quantity'] = total_quantity
        session['total_price'] = round(total_price, 2) # Since we're dealing with prices, we make sure the result we get only has 2 digits after the decimal point.
                                                                          
        cur.close()
        con.close()
        
        # We redirect back to the user home.
        return redirect(url_for('userhome'))

# The function below takes 2 arrays of type list,dict or set and merges them together.
# Source: Directly copy-pasted from the python file included with the Shopping Basket lab sheet from Week 5 of 5001CEM.
def array_merge( first_array , second_array ):
	if isinstance( first_array , list ) and isinstance( second_array , list ):
		return first_array + second_array
	elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
		return dict( list( first_array.items() ) + list( second_array.items() ) )
	elif isinstance( first_array , set ) and isinstance( second_array , set ):
		return first_array.union( second_array )
	return False		        


@app.route('/shoppingcart', methods=['POST'])
# The function below handles the POST request for the shopping cart page.
def shopping_cart():
    # If we get a POST request, we display the shopping cart page.
    if request.method == 'POST':
        return show_shopping_cart()

# The function below displays the shopping cart page.
def show_shopping_cart(): 
    return render_template('shoppingcart.html', page=url_for('shopping_cart'))


@app.route('/emptycart', methods=['POST'])
# The function below handles the POST request for the empty cart page.
def empty_cart():
    # If we get a POST request, we empty the shopping basket and redirect back to the user home page.
    if request.method == 'POST':        
        # To empty the shopping basket, we just clear the session.
        session.clear()
        return redirect(url_for('userhome'))

    
@app.route('/gobackhome', methods=['POST'])
# The function below handles the POST request for the go back home page.
def go_back_home():
    # If we get a POST request, we display the home page.
    if request.method == 'POST':
        return show_user_home_page()

    
@app.route('/deletebook', methods=['POST'])
# The function below handles the POST request for the delete book page.
def deletebook():
    # If we get a POST request, we remove the book from the shopping cart.
    if request.method == 'POST':
        # Here we request the value of the hidden input in the form that was submitted by the user and then we store it in 'isbn'.
        isbn = request.form.get('isbn_13') 
        # We check if the shopping cart has more than 1 books.
        if len(session['cart_book'].keys()) > 1:
            # If yes, we make sure to change the total price and quantity accordingly and then we remove the book from session.
            session['total_quantity'] = session['total_quantity'] - session['cart_book'][isbn]['occurence']
            session['total_price'] = round(session['total_price'] - session['total_quantity'] * session['cart_book'][isbn]['retail_price'], 2)
            del session['cart_book'][isbn]
            # We display the shopping cart page.
            return show_shopping_cart()
        else:
            # If not, we simply empty the shopping cart (by clearing the session).
            session.clear()
            # We show the home page instead of the shopping basket page, because the shopping cart is now empty anyways.
            return show_user_home_page()


        
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    