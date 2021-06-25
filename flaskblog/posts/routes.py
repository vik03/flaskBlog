from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Comment
from flaskblog.posts.forms import PostForm, CommentForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	posts_count = Post.query.count()
	form = PostForm()
	if form.validate_on_submit():
	    post = Post(title=form.title.data, problem=form.problem.data, root_cause=form.root_cause.data, content=form.content.data, author=current_user)
	    db.session.add(post)
	    db.session.commit()
	    flash('Your post has been created!', 'success')
	    return redirect(url_for('main.home'))
	return render_template('create_post.html', title='New Post',
	                       form=form, legend='New Post', posts_count=posts_count)


@posts.route("/post/<int:post_id>/comment", methods=['GET', 'POST'])
@login_required
def new_comment(post_id):
	posts_count = Post.query.count()
	comment = Comment.query.filter_by(post_id=post_id)
	post = Post.query.get_or_404(post_id)
	form = CommentForm()
	if form.validate_on_submit():
		comment = Comment(comment=form.comment.data, post_id=post_id, user_id=current_user.id)
		db.session.add(comment)
		db.session.commit()
		return redirect(url_for('posts.post',post_id=post_id))
	return render_template('create_comment.html', title='Create Comment',
	                       form=form, legend='Comment', posts_count=posts_count)


@posts.route('/add_Comment/<int:post_id>', methods=['GET', 'POST'])
@login_required
def add_comment(post_id):
	form = CommentForm()
	if form.validate_on_submit():
		comment = Comment(comment=form.comment.data, post_id=post_id, user_id=current_user.id)
		db.session.add(comment)
		db.session.commit()
		flash('Comment added Successfully', 'success')
		return redirect(url_for('main.home'))
	else:
		flash("Comment field cannot be Blank", 'danger')
		return redirect(url_for('main.home'))
	return render_template('home.html', form=form)


@posts.route("/post/<int:post_id>")
@login_required
def post(post_id):
	form = CommentForm()
	posts_count = Post.query.count()
	post = Post.query.get_or_404(post_id)
	comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.date_posted.desc())
	comment = Comment.query.order_by(Comment.date_posted.desc()).get(post_id)
	if form.validate_on_submit():
		comment = Comment(comment=form.comment.data, post_id=post.id, user_id=current_user.id)
		db.session.add(comment)
		db.session.commit()
		return redirect(url_for('posts.post',post_id=post.id))
	return render_template('post.html', title=post.title, post=post, comments=comments, posts_count=posts_count)



@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	posts_count = Post.query.count()
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
	    abort(403)
	form = PostForm()
	if form.validate_on_submit():
	    post.title = form.title.data
	    post.problem = form.problem.data
	    post.root_cause = form.root_cause.data
	    post.content = form.content.data
	    db.session.commit()
	    flash('Your post has been updated!', 'success')
	    return redirect(url_for('posts.post', post_id=post.id))
	elif request.method == 'GET':
	    form.title.data = post.title
	    form.problem.data = post.problem
	    form.root_cause.data = post.root_cause
	    form.content.data = post.content
	return render_template('create_post.html', title='Update Post',
	                       form=form, legend='Update Post', posts_count=posts_count)


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
	    abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted!', 'success')
	return redirect(url_for('main.home'))

