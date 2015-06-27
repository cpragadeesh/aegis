import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute("CREATE TABLE USERS(username TEXT, karma INTEGER, post_cout INTEGER, posts TEXT)")
c.execute("INSERT INTO USERS VALUES('admin', 0, 0, '')")
conn.commit()
conn.close()

