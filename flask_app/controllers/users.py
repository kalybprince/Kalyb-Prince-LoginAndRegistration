from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/login")
def login():
    print("/login")
    return render_template("login.html")

@app.route("/login/login_user", methods=["POST"])
def login_user():
    print("/login/login_user")
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/login")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/login')
    session['user_id'] = user_in_db.id
    return redirect("/login")

@app.route("/login/register_user", methods=["POST"])
def register_user():
    print("/login/register_user")

    if not User.passwords_match(request.form["password"], request.form["verify_password"]):
        return redirect(url_for('login'))
    if not User.validate_user(request.form):
        return redirect(url_for('login'))

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(f"Email and pass are valid!  Your hash is: {pw_hash}")

    data = {
        "email": request.form['email'],
        "password" : pw_hash
    }
    user_id = User.save(data)

    session["user_id"] = user_id

    return redirect("/login")