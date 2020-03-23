from app import db , app , login_manager , login_required , login_user , logout_user , mail , Message
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
        return render_template('/user/index.html', reg = reg , listAll = listAll , listShort = listShort)
    except:
        return render_template('/user/index.html')
    
@app.route("/register")
def register():
    return render_template('/user/egister.html')

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
            return render_template('/admin/admin.html', reg = reg)
        except:
            return render_template('/admin/admin.html') 

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
        send_Email(reg_teamname,None,reg_email,None,"Payment")
        return redirect("/admin")
    else:
        return render_template('/admin/register_team.html')

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
        listAgeGroup = ['Under 9 Mixed' , 'Under 11 Mixed', 'Under 13 Boys','Under 13 Girls' , 'Under 15 Boys', 'Under 15 Girls','Under 19 Boys' , 'Under 19 Girls', "Womens Open"]
        return render_template('/admin/edit.html', reg = reg , listAgeGroup = listAgeGroup , default = reg.ageGroup)

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
                return redirect("/login")
        else:
            flash('Invalid Username or Password.')
            return redirect("/login") 
    else:
        return render_template('/admin/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect('/login')

@app.route("/admin/registrationEmail", methods = ['POST','GET'])
@login_required
def registration_Email():
    url = 'registrationEmail'
    if request.method == 'POST':
        try:
            reg_teamname = request.form['teamname']
            reg_acceptDeny = request.form['acceptDeny']
            reg_email = request.form['email']
            reg_notes = request.form['notes']
            send_Email(reg_teamname,reg_acceptDeny,reg_email,reg_notes,"reg_email")
            return redirect("/admin")
        except:
            return redirect("/admin")
    else:
        label = 'Registration Email'
        return render_template('/admin/sendEmail.html', label = label , url=url)

#Modify Email Contents
def send_Email(team_name,action,email,notes,emailType):
    try:
        if emailType == "reg_email":
            if action == 'Accept':
                subjectHeader = 'Registration Accepted, Kiwanis Futbol Festival 2020'
                msgBody = f'Your Registration to Kiwanis Futbol Festival 2020 with the team { team_name } was accepted. Please send your payment immediately so that you will be Officially Registered. \n Payment details can be seen in the website in the registration form. \n {notes} \n Thank you'
            else:
                subjectHeader = 'Registration Rejected, Kiwanis Futbol Festival 2020'
                msgBody = f'Your Registration to Kiwanis Futbol Festival 2020 was Rejected, \n Reason: { notes }'    
        else:
            subjectHeader = 'Payment for Kiwanis Futbol Festival 2020 Recieved'
            msgBody = f'Your Payment for Kiwanis Futbol Festival 2020 with the team { team_name } was accepted. \n Your team is now officially registered, you may verify in our website under the tab "Registered Teams". \n { notes} \n Thank you'
        msg = Message(body = msgBody, sender='kiwanisfutbol@gmail.com',recipients=[email], subject= subjectHeader)
        mail.send(msg)
    except:
        print('Error in sending Email')

"""
#For creation of Admin Account
@app.route("/signup" , methods =  ['GET' , 'POST'])
def signup():
    password_hash = generate_password_hash('2020futbol' , method='sha256')
    user = Admin(username = 'kiwanisfutbol' , password = password_hash)
    db.session.add(user)
    db.session.commit()
    return render_template('index.html')
"""

    
