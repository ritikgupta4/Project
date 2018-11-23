from flask import render_template, url_for, flash, redirect, request
#To build a URL to a specific function, use the url_for() function. It accepts the name of the function as its first argument 
# and any number of keyword arguments, each corresponding to a variable part of the URL rule. 
# Unknown variable parts are appended to the URL as query parameters.

from eduSite import app, db   #the app instance of class Flask is created in __init__.py

from eduSite.forms import loginForm, signupForm, PostForm, CommentForm
from eduSite.models import User, Post, Comment 
      
from flask_login import login_user, current_user, logout_user, login_required      #https://flask-login.readthedocs.io/en/latest/



@app.route('/')                      #route() decorator to bind a function to a URL   #http://flask.pocoo.org/docs/1.0/api/#flask.Flask.route
@app.route('/home')
def home():
    posts = Post.query.all()
    comments = Comment.query.all()
    return render_template('home.html', posts=posts, comments=comments)

@app.route('/activity')
def activity():
    return render_template('activity.html')


#route(rule, **optons)

@app.route('/login', methods=['GET', 'POST']) #GET: Sends data in unencrypted form to the server.      POST:send HTML form data to server
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        password = User.query.filter_by(password=form.password.data).first()
        if user and password:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password')

    return render_template('login.html', form=form)

db.create_all()
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = signupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
              
        flash(f'Hey {form.username.data}! Your account has been created ')     #remember to add {form.role.data} eg. your student account has been created
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required   #???
def account():
    return render_template('account.html')


@app.route('/new_post', methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post published!')
        return redirect(url_for('home'))
    return render_template('create_post.html',title='New Post',form=form, legend='New Post')

@app.route("/post/<int:post_id>", methods=['GET','POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, poco=post)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added!')
        return redirect(url_for('home'))
    return render_template('post.html', poco=post, form=form,post=post)
