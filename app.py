import collections
import os
import string
from datetime import datetime
from typing import List, Optional

from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DATABASE_URL = os.environ['DATABASE_URL']
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)

# commands to be used
# User.query.all()
# User.query.filter_by(username='admin').first()
# {variable} = User(username='admin', email='admin@example.com', password='')
# db.session.add({variable})
# db.session.delete({variable})
# db.session.commit()
# py = Category(name='Python')
# Post(title='Hello Python!', body='Python is pretty cool', category=py)
# Post.query.with_parent(some_tag)


post_tags = db.Table('tags',
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
                     )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow)
    is_public = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
    user = db.relationship('User',
                           backref=db.backref('posts', lazy=True))
    tags = db.relationship('Tag', secondary=post_tags, lazy='subquery',
                           backref=db.backref('pages', lazy=True))

    def __repr__(self):
        return f'Post: {self.title}; {self.body}; {self.pub_date}'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Tag %r>' % self.name


def reset_db():
    db.drop_all()
    db.create_all()


@app.route('/')
def home(posts: Optional[List] = None, err: str = ""):
    print('rendering home page')
    user_id = request.cookies.get('userID')
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        print(user.posts)
        if posts is None:
            posts = user.posts

    return render_template('homepage.html',
                           user=user,
                           posts=posts,
                           login_error=err)


@app.route('/login', methods=['GET', 'POST'])
def login():
    print("logging in")
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    resp = make_response(render_template('set-cookie.html'))
    if not user:
        err = "username not registered"
        print(err)
        resp = home(err=err)
    elif user.password != password:
        err = "password incorrect"
        print(err)
        resp = home(err=err)
    else:
        print("login successful")
        resp.set_cookie('userID', str(hash(user.id)))
    return resp


@app.route('/register_page')
def render_register_page(err=""):
    return render_template('register_page.html', error=err)


@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    print(password)
    resp = make_response(render_template('set-cookie.html'))
    if User.query.filter_by(username=username).first():
        err = 'username already used'
        resp = render_register_page(err)
        return resp
    else:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        resp.set_cookie('userID', str(hash(user.id)))
    return resp


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    title = request.form['title']
    body = request.form['body']
    tags = request.form['tags']
    print(title + "\n" + body + "\n" + tags)
    user_id = request.cookies.get('userID')
    user = User.query.filter_by(id=user_id).first()
    tags = tags.split()
    post = Post(title=title, body=body, user=user)
    for tag_name in tags:
        tag_name = tag_name.translate(str.maketrans("", "", string.punctuation)).lower()
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag is None:
            tag = Tag(name=tag_name)
        post.tags.append(tag)
    db.session.add(post)
    db.session.commit()
    return render_template('set-cookie.html')


@app.route('/search-posts', methods=['GET', 'POST'])
def search_posts():
    search = request.form['']
    keywords = search.split()
    matches = []

    for keyword in keywords:
        matches.append(Post.query.filter(Post.title.like(f"%{keyword}%")))
        matches.append(Post.query.filter(Post.body.like(f"%{keyword}%")))
        matches.append(Post.query.filter(Post.user.username.like(f"%{keyword}%")))
        matches.append(Post.query.filter(Post.tags.name.like(f"%{keyword}%")))

    counts = collections.Counter(matches)
    posts = list(set(sorted(matches, key=lambda x: -counts[x])))
    home(posts)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ['PORT']))
