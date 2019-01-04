from flask import Flask,render_template,redirect,session,request,\
flash,redirect,url_for,g
import sqlite3
DATABASE="blog.db"
USERNAME="admin"
PASSWORD="admin"
SECRET_KEY="b'~\x8e!p\xffJ\x93\xfa\xaf\xaf\xc45{\x01\xe0a\xf8\x8f\x02\xf20\x99\xf7G'"
app=Flask(__name__)
app.config.from_object(__name__)
def connect_db():
	sqlite3.connect(app.config['DATABASE'])
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
def main():
	return render_template("main.html")	

if __name__=='__main__':
	app.run(debug=True)

