from flask import Flask, render_template

# Flask instance creation
app = Flask(__name__)


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