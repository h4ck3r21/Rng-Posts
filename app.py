import os
from datetime import datetime

from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DATABASE_URL = os.environ['DATABASE_URL']
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)


# commands to be used
# db.create_all()
# User.query.all()
# User.query.filter_by(username='admin').first()
# {variable} = User(username='admin', email='admin@example.com', password='xxxxxx')
# db.session.add({variable})
# db.session.delete({variable})
# db.session.commit()
# py = Category(name='Python')
# Post(title='Hello Python!', body='Python is pretty cool', category=py)


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

    def __repr__(self):
        return f'Post: {self.title}; {self.body}; {self.pub_date}'


@app.route('/')
def home():
    print('rendering home page')
    user_id = request.cookies.get('userID')
    err = request.cookies.get('login-error')
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        print(user.posts)
    return render_template('homepage.html', user=user, login_error=err)


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
        resp.set_cookie("login-error", err)
    elif user.password != password:
        err = "password incorrect""password incorrect"
        print(err)
        resp.set_cookie("login-error", err)
    else:
        print("login successful")
        resp.set_cookie('userID', str(user.id))
    return resp


@app.route('/register_page')
def render_register_page():
    return render_template('register_page.html', error="")


@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    resp = make_response(render_template('set-cookie.html'))
    if User.query.filter_by(username=username).first():
        err = 'username already used'
        resp.set_cookie("login-error", err)
        return resp
    else:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        resp.set_cookie('userID', str(user.id))
    return resp


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    title = request.form['title']
    body = request.form['body']
    print(title + "\n" + body)
    user_id = request.cookies.get('userID')
    user = User.query.filter_by(id=user_id).first()
    post = Post(title=title, body=body, user=user)
    db.session.add(post)
    db.session.commit()
    return render_template('set-cookie.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ['PORT']))
