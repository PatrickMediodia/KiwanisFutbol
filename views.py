from app import app
from app import db
from flask import Flask, escape, request , render_template , request,redirect
from models import Registered,Admin
from werkzeug.security import generate_password_hash

@app.route("/")
def index():
    try:
        listAll = [['Under 9 Mixed' , 'Under 11 Mixed', 'Under 13 Boys'], ['Under 13 Girls' , 'Under 15 Boys', 'Under 15 Girls'],['Under 19 Boys' , 'Under 19 Girls', "Women's Open"]]
        reg = Registered.query.order_by(Registered.date_registered).all()
        return render_template('index.html', reg = reg , listAll = listAll)
    except:
        return render_template('index.html')
    
@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/admin", methods = ['POST','GET'])
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
def registerteam():
    if request.method == 'POST':
        reg_teamname = request.form['teamname']
        reg_agegroup = request.form['agegroup']
        reg_email = request.form['email']
        new_reg = Registered(team_name = reg_teamname, ageGroup = reg_agegroup , email = reg_email)
        db.session.add(new_reg)
        db.session.commit()
        return redirect("/admin")
    else:
        return render_template('register_team.html')

@app.route("/admin/delete/<int:id>")
def delete(id):
    reg = Registered.query.get_or_404(id)
    db.session.delete(reg)
    db.session.commit()
    return redirect("/admin")

@app.route("/admin/edit/<int:id>" , methods =  ['GET' , 'POST'])
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
    pass