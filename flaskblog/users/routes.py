from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (LoginForm, UpdateAccountForm)
from flaskblog.users.utils import save_picture


users = Blueprint('users', __name__)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))




@users.route("/loginss", methods=['GET', 'POST'])
def loginss():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('main.home'))

        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	posts_count = Post.query.count()
	current_user_post_count = Post.query.filter_by(author=current_user).count()
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
		    picture_file = save_picture(form.picture.data)
		    current_user.image_file = picture_file
		#current_user.username = form.username.data
		db.session.commit()
		flash('Your account has been updated!', 'success')
		return redirect(url_for('users.account'))
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account',
	                       image_file=image_file, form=form, current_user_post_count=current_user_post_count, posts_count=posts_count)


@users.route("/user/<string:username>")
@login_required
def user_posts(username):
	posts_count = Post.query.count()
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('user_posts.html', posts=posts, user=user, posts_count=posts_count)