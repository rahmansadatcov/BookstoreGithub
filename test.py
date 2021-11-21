import sqlite3


def test():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    
    cur.execute('SELECT title, isbn_13, qty, cover FROM books')
    result = cur.fetchall()
    
    print(result[0])
    
    cur.close()
    con.close()

test()
