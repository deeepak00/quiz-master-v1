from flask import Flask, render_template, request, url_for, redirect,session
from flask import current_app as app
from datetime import datetime
import matplotlib.pyplot as plt


from .models import *



@app.route("/", methods=['GET','POST'])
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        type = request.form.get('type')
        if type=="admin":
            admin = Admin.query.first()
            if admin:
                if (admin.username==username and admin.password==password):
                    return redirect('/admin_dash')
                return render_template('wrong_admin_credentials.html')
            return render_template('not_exist.html', msgto='admin')
        if type=="user":
            user = User.query.filter(User.username==username).first()
            if user:
                if user.password==password:
                    return redirect(f'/user_dash/{user.id}')
                return render_template('wrong_user_credentials.html')
            return render_template('not_exist.html', msgto='user')
    return render_template('login.html')

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        qualification = request.form.get('qualification')
        dob = datetime.strptime(request.form.get('dob'), "%Y-%m-%d").date() 

        exist = User.query.filter(User.username==username).first()
        if not exist:
            new_user = User(username=username,password=password,full_name=full_name,qualification=qualification,dob=dob)
            db.session.add(new_user)
            db.session.commit()
            return 'Registration Successfull. Now login'
        return 'Already Exist username. Try registreing with New username'
    return render_template("register.html")





