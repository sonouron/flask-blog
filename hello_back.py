from crypt import methods
from enum import unique
from operator import pos
from flask import Flask, redirect, render_template, flash, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime,date
from werkzeug.security import generate_password_hash,check_password_hash
from wtforms.widgets import TextArea
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user,current_user

# Flask instance creation
app = Flask(__name__)
# Add database
# Sqlite db
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'

# Secret Key!!!
app.config['SECRET_KEY']="sonou"

#Initialize the database
db=SQLAlchemy(app)
migrate = Migrate(app,db)

# Flask Login 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))



"""
Blog post
"""
# Create a blog post Model
class Posts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(250))
    author = db.Column(db.String(250))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime,default=datetime.utcnow)
    slug = db.Column(db.String(250))


# Create Post form 
class PostForm(FlaskForm):
    title = StringField("Titre",validators=[DataRequired()])
    content = StringField("Contenu",validators=[DataRequired()], widget=TextArea())
    author = StringField("Auteur",validators=[DataRequired()])
    slug = StringField("Slug",validators=[DataRequired()])
    submit = SubmitField("Poster")


# Post page
@app.route('/add-posts',methods=["GET","POST"])
#@login_required
def add_posts():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(title = form.title.data, content=form.content.data, author=form.author.data, slug= form.slug.data )
        # Clear The form
        form.title.data =''
        form.content.data=''
        form.author.data = ''
        form.slug.data = ''
        
        # Add post to database
        db.session.add(post)
        db.session.commit()
        # Return message
        flash("Article enr??gistrer avec succ??s")
    return render_template("add_post.html",form = form)


# Show blog posts
@app.route('/posts')
def posts():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template('posts.html',posts=posts)

# Show Individual Blog post
@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html',post=post)

# Edit blog post 
@app.route('/posts/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data

        db.session.add(post)
        db.session.commit()
        flash("L'article a ??t?? modifier avec succ??s")
        return redirect(url_for('post',id=post.id))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html',form=form)

# Delete a blog post
@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post_to_delete=Posts.query.get_or_404(id)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash('Article supprimer avec succ??s')
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html',posts=posts)

    except:
        flash('Erreur!! Veillez r??essayer!!')
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html',posts=posts)

""" 
Blog post end
""" 

# Create Users Model on database
class Users(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(120), nullable = False, unique=True)
    color = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
    # Ajout du mot de passe
    password_hash = db.Column(db.String(120))

    @property
    def password(self):
        raise AttributeError("Le mots de passe ne peut ??tre lu")
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_pwd(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<Name %r>' % self.name

# Create a form class
class UserForm(FlaskForm):
    name = StringField("Nom", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    color = StringField("Color")
    password_hash = PasswordField("Password",validators=[DataRequired(),EqualTo('password_hash2',message='Saisissez le m??me mot de passe')])
    password_hash2 = PasswordField("Confirm Password",validators=[DataRequired()])
    submit = SubmitField("Envoyer")


# Create a form class
class NamerForm(FlaskForm):
    name = StringField("Quel est votre nom?", validators=[DataRequired()])
    submit = SubmitField("Envoyer")

# Create a password form class
class PasswordForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired()])
    password_hash = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField("Connexion")


# Json using

@app.route('/date')
def get_date():
    favorites_pizza = {
        'John' : 'Pepperonni',
        'Ronald': 'Avocat',
        'Miroire' : 'Glace',
    }
    return favorites_pizza
    #return {'Date':date.today()}

# Delete user in database
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete=Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('Utilisateur supprimer avec succ??s!!!')
        our_users = Users.query.order_by(Users.date_added)
        return render_template('add_user.html',form=form,name=name,our_users=our_users)
    except:
        flash('Oups!! R??essayer...')
        return render_template('add_user.html',form=form,name=name,our_users=our_users)


# Update Database
@app.route('/update/<int:id>',methods=["GET","POST"])
def update(id):
    form = UserForm()
    user_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        user_to_update.name = request.form['name']
        user_to_update.email = request.form['email']
        user_to_update.color = request.form['color']
        user_to_update.username = request.form['username']

        try:
            db.session.commit()
            flash("Utilisateur modifier avec succ??s")
            return render_template('update.html', form = form, user_to_update=user_to_update,id=id)
        except:
            flash("Erreur, r??essayer!!!")
            return render_template('update.html', form = form, user_to_update=user_to_update,id=id)
    else:
        return render_template('update.html', form = form, user_to_update=user_to_update,id=id)

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

"""
Login 
"""
# Loginform
class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Se connecter")

# Login page 
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # Check the hash
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                flash("Connexion r??ussit")
                return redirect(url_for('dashboard'))
            else:
                flash("Mot de passe incorrect. R??essayer")
        else:
            flash("Cet utilisateur n'est pas enr??gistrer")
    return render_template('login.html',form=form)

# Dashboard Page
@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    user_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        user_to_update.name = request.form['name']
        user_to_update.email = request.form['email']
        user_to_update.color = request.form['color']
        user_to_update.username = request.form['username']

        try:
            db.session.commit()
            flash("Utilisateur modifier avec succ??s")
            return render_template('dashboard.html', form = form, user_to_update=user_to_update,id=id)
        except:
            flash("Erreur, r??essayer!!!")
            return render_template('dashboard.html', form = form, user_to_update=user_to_update,id=id)
    else:
        return render_template('dashboard.html', form = form, user_to_update=user_to_update,id=id)   
    return render_template('dashboard.html')

# Logout page
@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("D??connexion r??ussit")
    return redirect(url_for('login'))



# User geting page
@app.route('/user/add',methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        hashed_pwd = generate_password_hash(form.password_hash.data,"sha256")
        if user is None:
            user = Users(name=form.name.data,username=form.username.data,email=form.email.data,color=form.color.data, password_hash = hashed_pwd)
            db.session.add(user)
            db.session.commit()
        name = form.name.data 
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.color.data = ''
        form.password_hash.data = ''
        
        flash('Utilisateur enr??gistrer avec succ??s!!!')
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
@app.route('/test_pwd',methods=['GET','POST'])
def test_pwd():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    #Form validation
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        form.email.data = ''
        form.password_hash.data = ''
        # Get users infos in db
        pw_to_check = Users.query.filter_by(email=email).first()
        # Check hashed password
        passed = check_password_hash(pw_to_check.password_hash,password)

    return render_template('test_pwd.html',email = email,form = form, passed=passed, password= password, pw_to_check = pw_to_check)


# Create page for getings name
@app.route('/name',methods=['GET','POST'])
def name():
    name = None
    form = NamerForm()
    #Form validation
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Envoyer avec succ??s!!!')
    return render_template('name.html',name = name,form = form)