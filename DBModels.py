from datetime import datetime

from app import db

post_tags = db.Table('tags',
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
                     )

category_posts = db.Table('posts',
                          db.Column('post_id', db.Integer,
                                    db.ForeignKey('post.id'),
                                    primary_key=True),
                          db.Column('category_id',
                                    db.Integer,
                                    db.ForeignKey('category.id'),
                                    primary_key=True),
                          )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Permissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('permissions', lazy=True))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('permissions', lazy=True))
    canPost = db.Column(db.Boolean, nullable=False, default=False)
    canDelete = db.Column(db.Boolean, nullable=False, default=False)
    canView = db.Column(db.Boolean, nullable=False, default=False)
    canTimeout = db.Column(db.Boolean, nullable=False, default=False)
    canAttachFiles = db.Column(db.Boolean, nullable=False, default=False)
    canMute = db.Column(db.Boolean, nullable=False, default=False)
    canBan = db.Column(db.Boolean, nullable=False, default=False)
    canPromote = db.Column(db.Boolean, nullable=False, default=False)
    canModify = db.Column(db.Boolean, nullable=False, default=False)
    CanInvite = db.Column(db.Boolean, nullable=False, default=False)
    level = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<%r's Permissions in %r>" % (self.user, self.category)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    is_public = db.Column(db.Boolean, nullable=False, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref=db.backref('category', lazy=True))
    posts = db.relationship('Post', secondary=category_posts, lazy='subquery',
                            backref=db.backref('category', lazy=True))

    def __repr__(self):
        return '<Category %r: %r>' % (self.id, self.name)

    def __str__(self):
        return '<Category %r: %r>' % (self.id, self.name)


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
                           backref=db.backref('posts', lazy=True))

    # category = db.relationship('Category', secondary=category_posts, lazy='subquery', backref=db.backref)

    def __repr__(self):
        return '<Post %r>' % self.id

    def __str__(self):
        return '<Post %r: %r>' % (self.id, self.name)


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

    def __repr__(self):
        return "<File %r>" % self.name

