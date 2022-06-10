from crypt import methods
from enum import unique
from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Flask instance creation
app = Flask(__name__)
# Add database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
# Secret Key!!!
app.config['SECRET_KEY']="sonou"

#Initialize the database
db=SQLAlchemy(app)

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(120), nullable = False, unique=True)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name

# Create a form class
class UserForm(FlaskForm):
    name = StringField("Nom", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Envoyer")


# Create a form class
class NamerForm(FlaskForm):
    name = StringField("Quel est votre nom?", validators=[DataRequired()])
    submit = SubmitField("Envoyer")

# Home page
@app.route('/')
@app.route('/index.html')
def index():
    first_name ="Ronald"
    stuff = 'This is a <strong>Bold</strong> text'
    favorites_pizza = ["Pepperoni", "Cheese","Magarita","Angeliqua",450]
    return render_template('index.html',
            first_name=first_name,
            stuff=stuff,
            favorites_pizza=favorites_pizza)

# User geting page
@app.route('/user/add',methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data,email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data 
        form.name.data = ''
        form.email.data = '' 
        flash('Utilisateur enrégistrer avec succès!!!')
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html',form=form,name=name,our_users=our_users)

# User page
@app.route('/user/<name>')
def user(name):
    return render_template('user.html',user_name=name)

#Create custom Error pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


# Create page for getings name
@app.route('/name',methods=['GET','POST'])
def name():
    name = None
    form = NamerForm()
    #Form validation
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Envoyer avec succès!!!')
    return render_template('name.html',name=name,form=form)