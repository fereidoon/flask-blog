from flask import Flask,render_template,redirect,session,request,\
flash,redirect,url_for,g
import sqlite3
from functools import wraps
DATABASE="blog.db"
USERNAME="admin"
PASSWORD="admin"
SECRET_KEY="b'~\x8e!p\xffJ\x93\xfa\xaf\xaf\xc45{\x01\xe0a\xf8\x8f\x02\xf20\x99\xf7G'"
app=Flask(__name__)
app.config.from_object(__name__)
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])
def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if "logged_in" in session:
			return test(*args, **kwargs)
		else:
			flash("You need to log in first.")
			return redirect(url_for("login"))
	return wrap	
@app.route("/", methods=["GET","POST"])
def login():
	error=None
	status_code=200
	if request.method =="POST":
		if request.form["username"] != app.config["USERNAME"] or \
		request.form["password"] != app.config["PASSWORD"]:
			error="invalid credential.please try again."
			status_code=401
		else:
			session["logged_in"] = True
			return redirect(url_for("main"))	
	return render_template("login.html",error=error),status_code
@app.route("/logout")
def logout():
	session.pop("logged_in",None)
	flash("You were logged out")
	return redirect(url_for("login"))
@app.route("/main")
@login_required
def main():
    g.db = connect_db()
    cur = g.db.execute("SELECT * FROM posts")
    posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template('main.html',posts=posts)
@app.route("/add",methods=["POST"])
@login_required
def add():
	title=request.form["title"]
	post=request.form["post"]
	if not title or not post:
		flash("all filed is requared,please try again")
		return redirect(url_for("main"))
	else:
		g.db=connect_db()
		g.db.execute('insert into posts (title, post) values (?, ?)',
        [request.form['title'], request.form['post']])
#		g.db.execute("INSERT INTO posts (title,post) value(?,?)",[title,post])
		g.db.commit()
		g.db.close()
		flash("Nwe entry was successfuly posted!")
		return redirect(url_for("main"))


if __name__=="__main__":
	app.run(debug=True)

