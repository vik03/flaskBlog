from flask import render_template, request, Blueprint
from flask_login import login_required
from flaskblog.models import Post, Comment
from flaskblog.posts.forms import CommentForm


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    posts_count = Post.query.count()
    form = CommentForm()
    return render_template('home.html', form=form, posts=posts, posts_count=posts_count)


@main.route("/about")
@login_required
def about():
    return render_template('about.html', title='About')


@main.route("/report")
@login_required
def report():
	all_data = inventory.query.all()
	return render_template('report.html', data=all_data, title='Report')