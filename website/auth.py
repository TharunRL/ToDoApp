from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db;
from flask_login import login_user,login_required,logout_user,current_user

auth= Blueprint('auth',__name__)


@auth.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form.get('email')
        lpassword=request.form.get('lpassword')

        user=User.query.filter_by(email=email).first()
        print(email,lpassword)
        if user:
            if check_password_hash(user.password,lpassword):
                flash("Logged in successfully!",category="success")
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect Password",category="error")
        else:
            flash('Email does not exist',category='error')
        
    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=["GET","POST"])
def sign_up():
    if request.method=="POST":
        email=request.form.get('email')
        username=request.form.get('username')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists",category="error")
        elif(len(email)<6):
            flash('Email is too small',category='error')
        elif(len(username)<4):
            flash('Username must be atlear 4 characters',category='error')
        elif(password1 != password2):
            flash('Password is not matching',category='error')
        elif len(password1)<8:
            flash('Password mismatch',category='error')
        else:
            print(password1)
            new_user=User(email=email,username=username,password=generate_password_hash(password1,method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('Account created',category='success')
            return redirect(url_for('views.home'))
    return render_template("sign-up.html",user=current_user)