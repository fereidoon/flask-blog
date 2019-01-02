import sqlite3
dic={"Good": "I\'m good.",
"Well":"I\'m well.",
"Excellent":"I\'m excellent.",
"Okay":"I\'m okay."}
with  sqlite3.connect("blog.db") as conn:
	c=conn.cursor()
	#c.execute("CREATE TABLE posts (title TEXT,post TEXT)")
	for key,value  in dic.items():
		c.execute("INSERT INTO posts VALUES (?,?)",(key,value))