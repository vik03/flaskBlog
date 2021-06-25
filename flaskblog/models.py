from datetime import datetime
from flaskblog import db, login_manager
from flask import current_app
from flask_login import UserMixin
import ldap


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_ldap_connection():
    conn = ldap.initialize(current_app.config['LDAP_PROVIDER_URL'])
    conn.protocol_version = ldap.VERSION3
    conn.set_option(ldap.OPT_REFERRALS, 0)
    return conn


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    signum = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='commenter', lazy='dynamic', cascade="all, delete, delete-orphan")

 
    def __repr__(self):
        return f"User('{self.username}', '{self.id}', '{self.image_file}', '{self.name}', '{self.signum}')"
 
    @staticmethod
    def try_login(username, password):
        conn = get_ldap_connection()
        bind = conn.simple_bind_s(username, password)
        if bind:
            base = "dc=ericsson, dc=se"
            criteria = "(&(mail={}))".format(username)
            attributes = ['displayName', 'eriSignumUpperCase']
            result = conn.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)
            for dn, entry in result:
                if isinstance(entry, dict):
                    name = entry['displayName']
                    signum = entry['eriSignumUpperCase']
                    name = [n.decode('utf-8') for n in name]
                    signum = [n.decode('utf-8') for n in signum]
                    name = name[0]
                    signum = signum[0]
                    return name, signum

 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return self.id


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    problem = db.Column(db.Text, nullable=False)
    root_cause = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    posts = db.relationship('Comment', backref='poster', lazy='dynamic', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"Post('{self.title}', '{self.problem}', '{self.root_cause}', '{self.date_posted}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Comment('{self.id}', '{self.comment}', '{self.post_id}', '{self.user_id}', '{self.date_posted}')"
