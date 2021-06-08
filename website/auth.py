from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user
auth=Blueprint('auth',__name__)
@auth.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                login_user(user,remember=True)
                flash("Logged in successfully!",category="success")
                return redirect(url_for('views.about_me'))
            else:
                flash("Incorrect password!Try again",category="error")
        else:
            flash("No such user exists",category="error")
    return render_template("login.html",user=current_user)

@auth.route('/sign-up',methods=["GET","POST"])
def sign_up():
    if request.method=="POST":
        email=request.form.get("email")
        firstname=request.form.get("firstname")
        password1=request.form.get("password1")
        password2=request.form.get("password2")
        user=User.query.filter_by(email=email).first()
        if user:
            flash("user already exists",category="error")
        elif password1!=password2:
            flash("passwords don\'t match",category="error")
        elif len(email)<4:
            flash("Email must be greater than 3 characters",category="error")
        elif len(firstname)<2:
            flash("name must be greater than 1 characters",category="error")
        elif len(password1)<7:
            flash("password must be greater than 6 characters",category="error")
        else:
            new_user=User(email=email,password=generate_password_hash(password1,method="sha256"),firstname=firstname)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash("Success! account created",category="success")
            return redirect(url_for('views.about_me'))

    return render_template("signup.html",user=current_user)
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/settings')
def settings():
    return render_template("settings.html",user=current_user)
