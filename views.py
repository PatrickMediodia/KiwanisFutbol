from app import db , app , login_manager , login_required , login_user , logout_user
from flask import Flask, escape, request , render_template , request, redirect , flash
from models import Registered,Admin
from werkzeug.security import generate_password_hash , check_password_hash

login_manager.login_view = "login"

@app.route("/")
def index():
    try:
        listShort = [ 'u9' , 'u11','u13Boys','u13Girls','u15Boys','u15Girls','u19Boys','u19Girls','Women']
        listAll = [['Under 9 Mixed' , 'Under 11 Mixed', 'Under 13 Boys'], ['Under 13 Girls' , 'Under 15 Boys', 'Under 15 Girls'],['Under 19 Boys' , 'Under 19 Girls', "Womens Open"]]
        reg = Registered.query.order_by(Registered.date_registered).all()
        return render_template('index.html', reg = reg , listAll = listAll , listShort = listShort)
    except:
        return render_template('index.html')
    
@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/admin", methods = ['POST','GET'])
@login_required
def admin():
    if request.method == 'POST':
        reg_teamname = request.form['teamname']
        reg_agegroup = request.form['agegroup']
        reg_email = request.form['email']
        new_reg = Registered(team_name = reg_teamname, ageGroup = reg_agegroup , email = reg_email)
        db.session.add(new_reg)
        db.session.commit()
        return redirect("/admin")
    else:
        try:
            reg = Registered.query.all() 
            return render_template('admin.html', reg = reg)
        except:
            return render_template('admin.html') 

@app.route("/admin/registerteam", methods = ['POST','GET'])
@login_required
def registerteam():
    if request.method == 'POST':
        reg_teamname = request.form['teamname']
        reg_agegroup = request.form['ageGroup']
        reg_email = request.form['email']
        new_reg = Registered(team_name = reg_teamname, ageGroup = reg_agegroup , email = reg_email)
        db.session.add(new_reg)
        db.session.commit()
        return redirect("/admin")
    else:
        return render_template('register_team.html')

@app.route("/admin/delete/<int:id>")
@login_required
def delete(id):
    reg = Registered.query.get_or_404(id)
    db.session.delete(reg)
    db.session.commit()
    return redirect("/admin")

@app.route("/admin/edit/<int:id>" , methods =  ['GET' , 'POST'])
@login_required
def edit(id):
    reg = Registered.query.get_or_404(id)
    if request.method == 'POST':
        reg.team_name = request.form['teamname']
        reg.ageGroup = request.form['agegroup']
        reg.email = request.form['email']
        db.session.commit()
        return redirect("/admin")   
    else:
        return render_template('edit.html', reg = reg)

@app.route("/login" , methods =  ['GET' , 'POST'])
def login():
    if request.method =='POST':
        user = Admin.query.filter_by(username = request.form['username']).first()
        password = request.form['password']
        if user: 
            if check_password_hash(user.password , password):
                login_user(user)
                return redirect("/admin") 
        else:
            flash('Invalid Username or Password.')
            return redirect("/admin") 
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect('/login')

"""
@app.route("/signup" , methods =  ['GET' , 'POST'])
def signup():
    password_hash = generate_password_hash('2020futbol' , method='sha256')
    user = Admin(username = 'kiwanisfutbol' , password = password_hash)
    db.session.add(user)
    db.session.commit()
    return render_template('index.html')
"""