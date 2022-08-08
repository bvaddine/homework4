from flask import Flask, render_template,request, redirect, session,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired, Length
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder='./')
app.config['SECRET_KEY'] = 'yellowkey'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'yellowdata.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

yellowdb = SQLAlchemy(app)
class Yellow(yellowdb.Model):
    __tablename__='yellow'
    id = yellowdb.Column(yellowdb.Integer, primary_key = True)
    name = yellowdb.Column(yellowdb.Text)
    email = yellowdb.Column(yellowdb.Text)
    addr = yellowdb.Column(yellowdb.Text)
    contact = yellowdb.Column(yellowdb.Text)
    def __init__(self,name,email,addr,contact):
        self.name = name
        self.email = email
        self.addr = addr
        self.contact = contact
    def __repr__(self):
        return f"{self.name} {self.email} {self.addr} {self.contact}"
yellowdb.create_all()

class Displayform(FlaskForm):
    add = SubmitField('ADD')
    delete = SubmitField('DELETE')
    update = SubmitField('UPDATE')

class Addform(FlaskForm):
    name = StringField('Comapany name:',validators=[DataRequired()])
    email = StringField('Comapany email:',validators=[DataRequired()])
    addr = StringField('Comapany address:',validators=[DataRequired()])
    contact = StringField('Comapany contact:',validators=[DataRequired()])
    add = SubmitField('ADD')

class Updateform(FlaskForm):
    name = StringField('Comapany name:',validators=[DataRequired()])
    email = StringField('Comapany email:',validators=[DataRequired()])
    addr = StringField('Comapany address:',validators=[DataRequired()])
    contact = StringField('Comapany contact:',validators=[DataRequired()])
    update = SubmitField('UPDATE')

@app.route('/',methods = ['GET','POST'])
def display():
    form = Displayform()
    if form.add.data:
        return redirect(url_for('add'))
    if form.update.data:
        upduser = request.form.get('delete')
        upddetails = Yellow.query.filter(Yellow.email == upduser).first()
        session['email'] = upddetails.email
        return redirect(url_for('update'))
    if form.delete.data:
        deluser = request.form.get('delete')
        deldetails = Yellow.query.filter(Yellow.email == deluser).first()
        yellowdb.session.delete(deldetails)
        yellowdb.session.commit()
        alldetails = Yellow.query.all()
        return render_template('display.html',disp = alldetails, error = None,form = form)

    alldetails = Yellow.query.all()
    return render_template('display.html',disp = alldetails, error =None,form = form)

@app.route('/add',methods = ['GET','POST'])
def add():
    form = Addform()
    if form.add.data:
        name = form.name.data
        email = form.email.data
        addr = form.addr.data
        contact = form.contact.data
        new = Yellow(name,email,addr,contact)
        yellowdb.session.add(new)
        yellowdb.session.commit()
        return redirect(url_for('display'))
    return render_template('add.html',form = form)

@app.route('/update',methods = ['GET','POST'])
def update():
    form = Updateform()
    if form.update.data:
        email = session['email']
        upduser = Yellow.query.filter(Yellow.email == email).first()
        upduser.name = form.name.data
        upduser.email = form.email.data
        upduser.addr = form.addr.data
        upduser.contact = form.contact.data
        yellowdb.session.add(upduser)
        yellowdb.session.commit()
        return redirect(url_for('display'))
    return render_template('update.html',form = form)

if __name__ == '__main__':
    app.run(debug=True)
