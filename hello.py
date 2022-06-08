from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired


# Flask instance creation
app = Flask(__name__)
app.config['SECRET_KEY']="sonou"

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