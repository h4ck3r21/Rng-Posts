from datetime import datetime

from app import db

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
