from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField


# Create a search form 
class SearchForm(FlaskForm):
    searched = StringField("Search",validators=[DataRequired()])
    submit = SubmitField("Rechercher")

# Create Post form 
class PostForm(FlaskForm):
    title = StringField("Titre",validators=[DataRequired()])
    # Add posts without rich text
    #content = StringField("Contenu",validators=[DataRequired()], widget=TextArea())
    # Add posts with rich text editor
    content = CKEditorField('Content',validators=[DataRequired()])
    #author = StringField("Auteur")
    slug = StringField("Slug",validators=[DataRequired()])
    submit = SubmitField("Poster")


# Create a form class
class UserForm(FlaskForm):
    name = StringField("Nom", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    color = StringField("Color")
    about_author = TextAreaField("About author")
    password_hash = PasswordField("Password",validators=[DataRequired(),EqualTo('password_hash2',message='Saisissez le même mot de passe')])
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


# Loginform
class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Se connecter")