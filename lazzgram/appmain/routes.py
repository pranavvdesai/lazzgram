import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from appmain import app, db, bcrypt
from appmain.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from appmain.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from appmain import ml
import pickle
from sqlalchemy import select
from sqlalchemy import create_engine


engine = create_engine('sqlite:///site.db')

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='about')
   


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created, you can login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username= form.username.data
        current_user.email= form.email.data
        db.session.commit()
        flash('you account has been updated','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile/' + current_user.image_file )
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data, content=form.content.data, author=current_user,user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('your post has been created','success')
        li=post.content
        ml.pr(li)
        res=ml.predict(li)
        if res['compound']>0.05:
            # positive sentiment
            print("Positive")
            id=post.user_id
            t1=User.query.get(id)
            t_count=current_user.token_count
            t1.token_count =t_count+20
            db.session.commit()
            print(t1.token_count)

        elif res['compound']>-0.05 and res['compound']<0.05:
            # neutral sentiment
            print("Neutral")
            id=post.user_id
            t1=User.query.get(id)
            t_count=current_user.token_count
            t1.token_count =t_count+5
            db.session.commit()
            print(t1.token_count)

        elif res['compound']<-0.05:
            #negative sentiment 
            print('Negative')   
            id=post.user_id
            t1=User.query.get(id)
            t_count=current_user.token_count
            f_count=current_user.flag_count
            t1.token_count =t_count-30
            t1.flag_count=f_count+1
            db.session.commit()
            print(t1.token_count)
            print(t1.flag_count)
        print(res)
        return redirect(url_for('home'))
    return render_template('create_post.html', title='new post', form=form)

def ret_str():
    return ss

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))