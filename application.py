#(venv) --- python application.py
#flask venv
from flask import Flask,render_template,redirect,url_for,request, jsonify, session, flash
from datetime import timedelta

app = Flask(__name__, static_folder = "assets")
app.secret_key = "Flask"
app.permanent_session_lifetime = timedelta(minutes=5)


userStore = [
	{"username": "admin", "password": "123"},
	{"username": "admin2", "password": "123"}
]

def response(data):
	jsonResult = [
		{"code": 403,"data": 'null', "message": "Register failed, Account had been created!"},
		{"code": 403,"data": 'null', "message": "Register failed, Username and password is the same!"},
		{"code": 200,"data": data, "message": "Register successful"},
		{"code": 200,"data": data, "message": "Login successful from Register"},
		{"code": 200,"data": data, "message": "Login successful from UserStorage"},
		{"code": 403,"data": 'null',"message": "Username or password are invalid"},
		{"code": 403,"data": 'null',"message": "Method not allowed"}
	]
	return jsonResult

@app.route("/index.html")
def home():
	return render_template("index.html")

@app.route("/cart.html")
def cart():
	return render_template("cart.html")

@app.route("/about.html")
def about():
	return render_template("about.html")

@app.route("/news.html")
def news():
	return render_template("news.html")

@app.route("/service.html")
def service():
	return render_template("/service.html")

@app.route("/contact.html")
def contact():
	return render_template("contact.html")

@app.route("/product.html")
def product():
	return render_template("/product.html")

@app.route("/login.html", methods=["POST", "GET"])
def login():
	# login
	if request.method == "POST":
		session_permanent = True
		username = request.form["username"]
		session["user"] = username
		flash("Login successful!")
		return redirect(url_for("user"))
	# else:
	# 	if "user" in session:
	# 		flash(f"{session['user']} already logged!")
	# 	return redirect(url_for("user"))
	return render_template("login.html")
		
@app.route("/logout")
def logout():
	session.pop("user", None)
	flash("You have been logout!")
	return redirect(url_for("login"))



@app.route("/user.html")
def user():
	if "user" in session:
		flash(f"Hi {session['user']}, you already logged!")
		return render_template("user.html")
	return redirect(url_for("login"))
	# return render_template("user.html")

@app.route("/api/auth/register", methods=["GET", "POST"])
def register():
	if request.method == "POST":
		session_permanent = True
		username = request.form["username"]
		password = request.form["password"]
		session["username"] = username
		session["password"] = password

		print(session["username"])
		print(session["password"])
				
		if username == password:
			return jsonify(response(request.form)[1])
		return jsonify(response(request.form)[2])
	return jsonify(response(request.form)[2])

@app.route("/api/auth/log-in", methods=["GET", "POST"])
def logIn():
	#GET request.args
	#POST request.form

	if request.method == "POST":
		session_permanent = True
		username = request.form['username']
		password = request.form['password']
		print(session['username'])
		print(session['password'])

		if (not hasattr(session, "username")):
			session["username"] = None			 

		if (not hasattr(session, "password")):
			session["password"] = None			    

		for user in userStore:
			# checking data user from register
			if (session["username"]  == username and session["password"] == password):
				return jsonify(response(request.form)[3])	
			# checking data user from datalocal
			if (username == user['username'] and password == user['password']):
				return jsonify(response(request.form)[4])
			
		return jsonify(response(request.form)[5])
	return jsonify(response(request.form)[6])


if __name__ == "__main__":
	app.run(debug = True)



