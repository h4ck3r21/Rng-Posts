from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

DATABASE_URL = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)


# commands to be used
# User.query.all()
# User.query.filter_by(username='admin').first()
# {variable} = User(username='admin', email='admin@example.com', password='xxxxxx')
# db.session.add({variable})
# db.session.delete({variable})
# db.session.commit()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def homepage():
    user_id = request.cookies.get('userID')
    print('rendering home page')
    # try:
    user = User.query.filter_by(id=user_id).first()
    return render_template('homepage.html', user=user)
    # except SQLAlchemy.exc.DataError:
    #   return render_template('homepage.html', user=None)


if __name__ == "__main__":
    app.run(debug=True)
