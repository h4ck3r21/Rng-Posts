import collections
import os
import string
from datetime import datetime
from typing import List, Optional

from flask import Flask, render_template, request, make_response, send_file, url_for, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'wav', }

DATABASE_URL = os.environ['DATABASE_URL']
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)

migrate = Migrate(app, db)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 10000000
app.secret_key = 'asdjlhkfuiewh32897re jhwqhyr8932ycrewyuqiyriuewoynq8392'

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
        return '<Post %r>' % self.id


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Tag %r>' % self.name


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    src = db.Column(db.String(400), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),
                        nullable=False)
    post = db.relationship('Post',
                           backref=db.backref('files', lazy=True))


def reset_db():
    db.drop_all()
    db.create_all()


@app.route('/')
def home(posts: Optional[List] = None, err: str = "", msg: str = ""):
    print('rendering home page')
    user_id = request.cookies.get('userID')
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        print(user.posts)
        if msg == "":
            msg = "Welcome " + user.username
        if posts is None:
            posts = user.posts

    return render_template('homepage.html',
                           msg=msg,
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


@app.route("/create-post")
def create_post():
    return render_template("send-post.html")


@app.route("/download_file/<path>/<filename>")
def download_file(path, filename):
    return send_file(path, download_name=filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        src = url_for('download_file', path=path, filename=filename)
        file_model = File(name=filename, src=src)
        return file_model
    else:
        flash('file type not accepted')
        return None


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        tags = request.form['tags']
        files = request.files.getlist('files[]')
        print(f"________________________{title}\n{body}\n{tags}\n{files}")
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
        for file in files:
            file_model = upload(file)
            if file_model is not None:
                post.files.append(file_model)
        db.session.add(post)
        db.session.commit()
        return render_template('set-cookie.html')
    else:
        return render_template('homepage.html')


@app.route("/post/<post_id>")
def display_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    print(f" -- {post.title} -- ")

    return render_template('posts.html', post_info={
        "title": post.title,
        "body": post.body,
        "time": "%s:%s %s/%s/%s" % (post.pub_date.hour,
                                    post.pub_date.minute,
                                    post.pub_date.day,
                                    post.pub_date.month,
                                    post.pub_date.year),
        "tags": " ".join([tag.name for tag in post.tags]),
        "user": post.user.username,
        "files": ",".join(map(lambda f: f.src, post.files))
    })


@app.route('/search-posts', methods=['GET', 'POST'])
def search_posts():
    search = request.form['search']

    keywords = search.split()
    posts = Post.query.all()
    post_value = {}
    for keyword in keywords:
        print(keyword)
        for post in posts:
            if post not in post_value:
                post_value[post] = assign_value(post, keyword)
            else:
                post_value[post] += assign_value(post, keyword)
    return home(sorted(posts, key=lambda p: post_value[p]), msg=f"Search results for '{search}'")


def old_search():
    search = request.form['search']
    print(search)
    keywords = search.split()
    matches = []

    for keyword in keywords:
        matches.extend(Post.query.filter(Post.title.like(f"%{keyword}%")).all())
        matches.extend(Post.query.filter(Post.body.like(f"%{keyword}%")).all())
        users = User.query.filter(User.username.like(f"%{keyword}%")).all()
        tags = Tag.query.filter(Tag.name.like(f"%{keyword}%")).all()
        for post in Post.query.all():
            if post.user in users:
                matches.append(post)
            tag_posts = [post for tag in post.tags if tag in tags]
            matches.extend(tag_posts)
    counts = collections.Counter(matches)
    posts = sorted(matches, key=lambda x: 10000 * x.pub_date.year + 100 * x.pub_date.month + x.pub_date.day,
                   reverse=True)
    print([p.pub_date for p in posts])
    posts = sorted(list(set(posts)), key=lambda x: -counts[x])
    return home(posts, msg=f"Search results for '{search}'")


def assign_value(post: Post, search):
    TITLE_VALUE = 3000000
    TAG_VALUE = 2000000
    BODY_VALUE = 1000000
    DATE_VALUE = 1
    value = 0
    value += post.title.count(search) * TITLE_VALUE
    value += [tag.name for tag in post.tags].count(search) * TAG_VALUE
    value += post.body.count(search) * BODY_VALUE
    value += (100000000 * post.pub_date.year +
              1000000 * post.pub_date.month +
              10000 * post.pub_date.day +
              100 * post.pub_date.hour +
              1 * post.pub_date.minute) * DATE_VALUE
    return value


@app.route("/logo")
def logo():
    return send_file("images/icon-turtle.jpg", mimetype='image/jpg')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ['PORT']))
