import os
from datetime import datetime

from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DATABASE_URL = os.environ['DATABASE_URL']
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
    user = db.relationship('User',
                           backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.title


@app.route('/')
def home():
    print('rendering home page')
    user_id = request.cookies.get('userID')
    user = User.query.filter_by(id=user_id).first()
    print(user)
    return render_template('homepage.html', user=user, login_error="")


@app.route('/login', methods=['GET', 'POST'])
def login():
    print("logging in")
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    resp = make_response(render_template('set-cookie.html'))
    if not user:
        print("username not registered")
        return render_template('homepage.html', user=None, login_error="username not registered")
    elif user.password != password:
        print("password incorrect")
        return render_template('homepage.html', user=None, login_error="password incorrect")
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
    if User.query.filter_by(username=username).first():
        return render_template('register_page.html', error='username already used')
    else:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        resp = make_response(render_template('set-cookie.html'))
        resp.set_cookie('userID', str(user.id))
        return resp


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    title = request.form['title']
    body = request.form['body']
    print(body)
    user_id = request.cookies.get('userID')
    user = User.query.filter_by(id=user_id).first()
    post = Post(title=title, body=body, user=user)
    db.session.add(post)
    #db.session.commit()
    return render_template('homepage.html', user=user, login_error="")


if __name__ == "__main__":
    app.run(debug=True)
