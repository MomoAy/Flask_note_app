from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint("auth", __name__)

@auth.route('/signup',methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template("auth/signup.html", user = current_user)
    else:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')
        user = Users.query.filter_by(email=email).first()
        if user : 
            flash("Email already exist", category="error")
            return redirect(url_for("auth.signup"))
        elif len(email) < 4 :
            flash("Email must be greater than 4 characters.", category="error")
            return redirect(url_for("auth.signup"))
        elif len(name) < 2 : 
            flash("Name must be greater than 2 characters.", category="error")
            return redirect(url_for("auth.signup"))
        elif password != repeat_password :
            flash("Password don't match.", category="error")
            return redirect(url_for("auth.signup"))
        elif len(password) < 7 :
            flash("Password must be greater than 7 characters.", category="error")
            return redirect(url_for("auth.signup"))
        else:
            new_user = Users(email=email, name = name, password = generate_password_hash(password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created", category="success")

        


        return redirect(url_for("views.home"))

@auth.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html", user = current_user)
    else:
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()
         
        if not user or not check_password_hash(user.password, password):
                flash('Please check your login details and try again.', category="error")
                return redirect(url_for('auth.login'))
        
        flash("Logged in successfuly !", category="success")
        login_user(user)

        return redirect(url_for("views.home"))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

