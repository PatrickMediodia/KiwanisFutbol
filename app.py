from flask import Flask, escape, request , render_template , request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registered.db'
db = SQLAlchemy(app)

class registered(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100),nullable =False)
    ageGroup = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date_registered = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return str(self.id)
    
@app.route("/")
def index():
    try:
        reg = registered.query.order_by(registered.date_registered).all()
        return render_template('index.html', reg = reg)
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
        new_reg = registered(team_name = reg_teamname, ageGroup = reg_agegroup , email = reg_email)
        db.session.add(new_reg)
        db.session.commit()
        return redirect("/admin")
    else:
        try:
            reg = registered.query.order_by(registered.date_registered).all() 
            return render_template('admin.html', reg = reg)
        except:
            return render_template('admin.html') 

@app.route("/admin/registerteam", methods = ['POST','GET'])
def registerteam():
    if request.method == 'POST':
        reg_teamname = request.form['teamname']
        reg_agegroup = request.form['agegroup']
        reg_email = request.form['email']
        new_reg = registered(team_name = reg_teamname, ageGroup = reg_agegroup , email = reg_email)
        db.session.add(new_reg)
        db.session.commit()
        return redirect("/admin")
    else:
        return render_template('register_team.html')

@app.route("/admin/delete/<int:id>")
def delete(id):
    reg = registered.query.get_or_404(id)
    db.session.delete(reg)
    db.session.commit()
    return redirect("/admin")

@app.route("/admin/edit/<int:id>" , methods =  ['GET' , 'POST'])
def edit(id):
    reg = registered.query.get_or_404(id)
    if request.method == 'POST':
        reg.team_name = request.form['teamname']
        reg.ageGroup = request.form['agegroup']
        reg.email = request.form['email']
        db.session.commit()
        return redirect("/admin")   
    else:
        return render_template('edit.html', reg = reg)

if __name__ == "__main__":
    app.run(debug=True) 