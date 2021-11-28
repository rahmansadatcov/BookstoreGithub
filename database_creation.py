import sqlite3

# The function below creates the 'admins' table in our database and then populates it.
def create_admins_table():
    con = sqlite3.connect('database.db')
    con.execute('CREATE TABLE admins (name TEXT, pwd INT)')
    con.close()
    
    con = sqlite3.connect('database.db')
    con.execute("INSERT INTO admins values(?,?);", ('admin', 'p455w0rd'))
    con.commit()
    con.close()

# The function below creates the 'books' table in our database and then populates it.
def create_users_table():
    con = sqlite3.connect('database.db')
    con.execute('CREATE TABLE users (name TEXT, pwd INT)')
    con.close()
    
    con = sqlite3.connect('database.db')
    con.execute("INSERT INTO users values(?,?);", ('customer1', 'p455w0rd'))
    con.execute("INSERT INTO users values(?,?);", ('customer2', 'p455w0rd'))
    con.commit()
    con.close()

# The function below creates the 'books' table in our database and then populates it.
def create_books_table():
    con = sqlite3.connect('database.db')
    con.execute('CREATE TABLE books (isbn_13 TEXT PRIMARY KEY, title TEXT, author TEXT, pub_date TEXT, retail_price REAL, trade_price REAL, qty INTEGER, cover TEXT, description TEXT)')
    con.close()
    
    con = sqlite3.connect('database.db')  
    con.execute("INSERT INTO books values(?,?,?,?,?,?,?,?,?);", ('9780450040184', 'The Shining', 'Stephen King', '01-07-1982', '4.06', '3.25', '13', 'cover_images/the-shining.jpg', 'Danny is only five years old, but he is a "shiner", aglow with psychic voltage. When his father becomes caretaker of an old hotel, his visions grow out of control. Cut off by blizzards, the hotel seems to develop an evil force, and who are the mysterious guests in the supposedly empty hotel?'))
    con.execute("INSERT INTO books values(?,?,?,?,?,?,?,?,?);", ('9780241341650', 'Nineteen Eighty-Four', 'George Orwell', '07-06-2018', '6.55', '4.89', '7', 'cover_images/nineteen-eighty-four.jpg', 'Hidden away in the Record Department of the sprawling Ministry of Truth, Winston Smith skilfully rewrites the past to suit the needs of the Party. Yet he inwardly rebels against the totalitarian world he lives in, which demands absolute obedience and controls him through the all-seeing telescreens and the watchful eye of Big Brother, symbolic head of the Party. In his longing for truth and liberty, Smith begins a secret love affair with a fellow-worker Julia, but soon discovers the true price of freedom is betrayal.'))
    con.execute("INSERT INTO books values(?,?,?,?,?,?,?,?,?);", ('9781473662070', 'Misery', 'Stephen King', '07-07-2011', '8.78', '6.99', '5', 'cover_images/misery.jpg', "Misery Chastain is dead. Paul Sheldon has just killed her - with relief, with joy. Misery has made him rich; she was the heroine of a string of bestsellers. And now he wants to get on to some real writing. That is when the car accident happens, and he wakes up in pain in a strange bed. But it isn't hospital. Annie Wilkes has pulled him from the wreck, brought him to her remote mountain home, splinted and set his mangled legs. The good news is that Annie was a nurse and has pain-killing drugs. The bad news is that she has long been Paul's Number One Fan. And when she finds out what Paul had done to Misery, she doesn't like it. She doesn't like it at all. Paul Sheldon used to write for a living. Now he's writing to stay alive."))
    con.execute("INSERT INTO books values(?,?,?,?,?,?,?,?,?);", ('9780552779777', 'The Girl On The Train', 'Paula Hawkins', '05-05-2016', '7.37', '5.22', '14', 'cover_images/the-girl-on-the-train.jpg', "Rachel catches the same commuter train every morning. She knows it will wait at the same signal each time, overlooking a row of back gardens. She's even started to feel like she knows the people who live in one of the houses. Jess and Jason, she calls them. Their life as she sees it is perfect. If only Rachel could be that happy. And then she sees something shocking. It's only a minute until the train moves on, but it's enough. Now everything's changed. Now Rachel has a chance to become a part of the lives she's only watched from afar. Now they'll see; she's much more than just the girl on the train."))
    con.execute("INSERT INTO books values(?,?,?,?,?,?,?,?,?);", ('9780241980354', 'East of Eden', 'John Steinback', '06-07-2017', '7.37', '5.78', '7', 'cover_images/east-of-eden.jpg', "California's fertile Salinas Valley is home to two families whose destinies are fruitfully, and fatally, intertwined. Over the generations, between the beginning of the twentieth century and the end of the First World War, the Trasks and the Hamiltons will helplessly replay the fall of Adam and Eve and the murderous rivalry of Cain and Abel.'"))
    con.execute("INSERT INTO books values(?,?,?,?,?,?,?,?,?);", ('9780349107035', 'Cosmos', 'Carl Sagan', '11-08-1983', '10.38', '7.97', '18', 'cover_images/cosmos.jpg', "The story of fifteen billion years of cosmic evolution transforming matter and life into consciousness, of how science and civilisation grew up together, and of the forces and individuals who helped shape modern science. A story told with Carl Sagan's remarkable ability to make scientific ideas both comprehensible and exciting."))
    con.execute("INSERT INTO books values(?,?,?,?,?,?,?,?,?);", ('9781529347852', 'Dune', 'Frank Herbert', '02-09-2021', '6.99', '4.25', '20', 'cover_images/dune.jpg', "Melange, or 'spice', is the most valuable - and rarest - element in the universe. And it can only be found on a single planet: the inhospitable desert world Arrakis. Whoever controls Arrakis controls the spice. And whoever controls the spice controls the universe. When stewardship of Arrakis is transferred to his house, Paul Atreides must travel to the planet's dangerous surface to ensure the future of his family and his people. But as malevolent forces explode into conflict around him, Paul is thrust into a great destiny beyond his understanding."))
    con.execute("INSERT INTO books values(?,?,?,?,?,?,?,?,?);", ('9781949759228', 'The Mountain Is You', 'Brianna Wiest', '29-05-2020', '11.45', '8.21', '10', 'cover_images/the-mountain-is-you.jpg', "This is a book about self-sabotage. Why we do it, when we do it, and how to stop doing it—for good. Coexisting but conflicting needs create self-sabotaging behaviors. This is why we resist efforts to change, often until they feel completely futile. But by extracting crucial insight from our most damaging habits, building emotional intelligence by better understanding our brains and bodies, releasing past experiences at a cellular level, and learning to act as our highest potential future selves, we can step out of our own way and into our potential.For centuries, the mountain has been used as a metaphor for the big challenges we face, especially ones that seem impossible to overcome. To scale our mountains, we actually have to do the deep internal work of excavating trauma, building resilience, and adjusting how we show up for the climb.In the end, it is not the mountain we master, but ourselves."))
    con.execute("INSERT INTO books values(?,?,?,?,?,?,?,?,?);", ('9781853267338', 'The Count of Monte Cristo', 'Alexandre Dumas', '05-11-1997', '2.25', '0.99', '8', 'cover_images/the-count-of-monte-cristo.jpg', "The story of Edmund Dantes, self-styled Count of Monte Cristo, is told with consummate skill. The victim of a miscarriage of justice, Dantes is fired by a desire for retribution and empowered by a stroke of providence. In his campaign of vengeance, he becomes an anonymous agent of fate. The sensational narrative of intrigue, betrayal, escape, and triumphant revenge moves at a cracking pace. Dumas' novel presents a powerful conflict between good and evil embodied in an epic saga of rich diversity that is complicated by the hero's ultimate discomfort with the hubristic implication of his own actions."))
    con.execute("INSERT INTO books values(?,?,?,?,?,?,?,?,?);", ('9781408848180', 'Paper Towns', 'John Green', '19-12-2013', '5.68', '3.20', '3', 'cover_images/paper-towns.jpg', "Quentin Jacobsen has always loved Margo Roth Spiegelman, for Margo (and her adventures) are the stuff of legend at their high school. So when she one day climbs through his window and summons him on an all-night road trip of revenge he cannot help but follow. But the next day Margo doesn't come to school and a week later she is still missing. Q soon learns that there are clues in her disappearance . . . and they are for him. But as he gets deeper into the mystery - culminating in another awesome road trip across America - he becomes less sure of who and what he is looking for. Masterfully written by John Green, this is a thoughtful, insightful and hilarious coming-of-age story."))
    con.commit()
    con.close()
    
# The function below deletes a book from the database if the value passed as an argument is the same as the value of the isbn attribute of that book.
# This function was used mainly for deleting records from 'books' after I was done troubleshooting the add_to_stock() function in the main python file.
def delete_row_from_books(i):
    con = sqlite3.connect('database.db')
    con.execute("DELETE FROM books WHERE isbn_13=(?)", (i,))
    con.commit()
    con.close()


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    