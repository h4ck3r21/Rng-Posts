import collections
import os
import string
from datetime import datetime
from typing import List, Optional

from flask import Flask, render_template, request, make_response, send_file, url_for, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename, redirect

app = Flask(__name__)
UPLOAD_FOLDER = 'files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'wav', 'mov', 'mkv'}
DEFAULT_USER_ID = 6

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL == None:
    DATABASE_URL = os.environ.get('POSTGRES_URL')
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
        return '<User%s %s>' % (self.id, self.username)


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
    followed = db.Column(db.Boolean, nullable=False, default=False)
    canInvite = db.Column(db.Boolean, nullable=False, default=False)
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


class InputError(Exception):
    pass


def reset_db():
    db.drop_all()
    db.create_all()


@app.route('/')
def home(items: Optional[List] = None, err: str = "", title: str = "", msg: str = "", category="None"):
    print('rendering home page')
    followed = "false"
    if err == "" or err is None:
        err = request.args.get('err')
        if err is None or err == "None":
            err = ""
    if msg == "" or msg is None:
        msg = request.args.get('msg')
        if msg is None or msg == "None":
            msg = ""
    user_id = request.cookies.get('userID')
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        print(user.posts)
        if title == "":
            title = request.args.get('title')
            if title is None:
                title = "Welcome " + user.username
        if items is None:
            items = user.posts
            categories = Category.query.filter_by(owner=user).all()
            permissions = Permissions.query.filter_by(user=user, followed=True).all()
            for permission in permissions:
                categories.append(permission.category)
            categories = list(set(categories))
            print(categories)
            items = categories + items
        if category is not None and category != "None":
            perm = Permissions.query.filter_by(user=user, category_id=category).first()
            if perm is not None:
                followed = perm.followed
    print("DEFAULT USERID:" + str(user_id))
    return render_template('homepage.html',
                           title=title,
                           msg=msg,
                           user=user,
                           posts=items,
                           login_error=err,
                           category=category,
                           followed=followed)


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
    elif user.username == "Default User":
        err = "username not allowed"
        print(err)
        resp = home(err=err)
    else:
        print("login successful")
        resp.set_cookie('userID', str(hash(user.id)))
    return resp

@app.route("/logout")
def logout():
    print("logging out")
    resp = make_response(render_template('set-cookie.html'))
    resp.delete_cookie('userID')
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
        # categories = request.form['categories']
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


# @app.route("/post/<post_id>", defaults={'category': False})
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
    categories = Category.query.all()
    post_value = {}
    category_value = {}
    for keyword in keywords:
        print(keyword)
        for post in posts:
            if post not in post_value:
                post_value[post] = assign_value(post, keyword)
            else:
                post_value[post] += assign_value(post, keyword)
        for category in categories:
            if category not in category_value:
                category_value[category] = category.name.count(keyword)
    print(post_value, sorted(posts, key=lambda p: post_value[p]), category_value, sep="\n***\n")
    results = sorted(categories, key=lambda c: category_value[c], reverse=True) + \
              sorted(posts, key=lambda p: post_value[p], reverse=True)
    return home(results, title=f"Search results for '{search}'")


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
    return home(posts, title=f"Search results for '{search}'")


def assign_value(post: Post, search):
    TITLE_VALUE = 300000000
    TAG_VALUE = 200000000
    BODY_VALUE = 100000000
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


@app.route("/category/<category_id>")
def view_category(category_id):
    user_id = request.cookies.get('userID')
    if user_id is None:
        return redirect(url_for("home", err="You need to sign in to perform this action"), code=302)
    user = User.query.filter_by(id=user_id).first()
    cat = Category.query.filter_by(id=category_id).first()
    permission = Permissions.query.filter_by(user=user, category=cat).first()
    if permission is None:
        permission = create_permission(user, cat)
    if user is not None and permission.canView:
        return home(cat.posts, title=cat.name, err=request.args.get('err'), category=category_id)
    else:
        return redirect(url_for("home", err="you do not have permission to view this category"), code=302)


def create_permission(user, category):
    print(f"new permission:{user}, {category}")
    if user is None:
        redirect(url_for("home", err="You need to sign in to perform this action"), code=302)
    default = Permissions.query.filter_by(user_id=DEFAULT_USER_ID).first()
    if default is None:
        default = create_default_permission(category)
    perms = Permissions(
        user=user,
        category=category,
        canPost=default.canPost,
        canDelete=default.canDelete,
        canView=default.canView,
        canTimeout=default.canTimeout,
        canAttachFiles=default.canAttachFiles,
        canMute=default.canMute,
        canBan=default.canBan,
        canPromote=default.canPromote,
        followed=default.followed,
        canInvite=default.canInvite,
        level=default.level
    )
    db.session.add(perms)
    db.session.commit()
    print("new perm:", perms)
    return perms

def create_default_permission(category):
    user = User.query.filter_by(id=DEFAULT_USER_ID).first()
    perms = Permissions(
        user=user,
        category=category,
        canPost=False,
        canDelete=False,
        canView=False,
        canTimeout=False,
        canAttachFiles=False,
        canMute=False,
        canBan=False,
        canPromote=False,
        followed=False,
        canInvite=False,
        level=100
    )
    if category.is_public:
        perms.canView = True
    db.session.add(perms)
    db.session.commit()
    print("new default perm:", perms)
    return perms

@app.route("/create-category", methods=["GET", "POST"])
def create_category():
    if request.method == 'POST':
        name = request.form['name']
        publicity = request.form['publicity']
        if publicity == "public":
            is_public = True
        elif publicity == "private":
            is_public = False
        else:
            raise InputError(f"unknown publicity: {publicity}")

        print(f"new category:{name}")
        user_id = request.cookies.get('userID')
        user = User.query.filter_by(id=user_id).first()
        cat = Category(name=name, is_public=is_public, owner=user)
        perms = Permissions(
            user=user,
            category=cat,
            canPost=True,
            canDelete=True,
            canView=True,
            canTimeout=True,
            canAttachFiles=True,
            canMute=True,
            canBan=True,
            canPromote=True,
            followed=True,
            canInvite=True,
            level=0
        )
        create_default_permission(cat)
        db.session.add(perms)
        db.session.commit()
        return redirect(url_for("view_category",
                                category_id=cat.id),
                        code=302)
    else:
        return render_template('homepage.html')


@app.route("/add-cat", methods=["GET", "POST"])
def add_post_to_category():
    if request.method == 'POST':
        post_id = request.form['post']
        post = Post.query.filter_by(id=post_id).first()
        cat_id = request.form['category']
        cat = Category.query.filter_by(id=cat_id).first()
        user_id = request.cookies.get('userID')
        user = User.query.filter_by(id=user_id).first()
        perms = Permissions.query.filter_by(user=user, category=cat).first()
        if perms is None:
            perms = create_permission(user, cat)
        if perms.canPost and (perms.canAttachFiles or post.files == []):
            print(f"adding post, {post.title}, to category, {cat.name}.")
            cat.posts.append(post)
            db.session.commit()
            return redirect(url_for("view_category",
                                    category_id=cat_id),
                            code=302)
        elif not perms.canPost:
            return redirect(url_for("view_category",
                                    err="You do not have permission to post in that category",
                                    category_id=cat_id),
                            code=302)
        else:
            return redirect(url_for("select_post",
                                    err="You do not have permission to post media in that category",
                                    category_id=cat_id),
                            code=302)
    else:
        return render_template('set-cookie.html')


@app.route("/new-category")
def new_category():
    return render_template("create-category.html")


@app.route("/select-category/<action>")
def select_category(action):
    user_id = request.cookies.get('userID')
    if user_id is None:
        abort(401)
    user = User.query.filter_by(id=user_id).first()
    if action == "view":
        permissions = Permissions.query.filter_by(user=user, canView=True).all()
    elif action == "post":
        permissions = Permissions.query.filter_by(user=user, canPost=True).all()
    elif action == "delete":
        permissions = Permissions.query.filter_by(user=user, canDelete=True).all()
    elif action == "timeout":
        permissions = Permissions.query.filter_by(user=user, canTimeout=True).all()
    elif action == "mute":
        permissions = Permissions.query.filter_by(user=user, canMute=True).all()
    elif action == "ban":
        permissions = Permissions.query.filter_by(user=user, canBan=True).all()
    elif action == "promote":
        permissions = Permissions.query.filter_by(user=user, canPromote=True).all()
    elif action == "modify":
        permissions = Permissions.query.filter_by(user=user, followed=True).all()
    elif action == "modify roles":
        permissions = Permissions.query.filter_by(user=user, canPromote=True).all()
        permissions = [perm for perm in permissions if perm.CanPromote]
    elif action == "invite":
        permissions = Permissions.query.filter_by(user=user, canInvite=True).all()
        permissions = [perm for perm in permissions if perm.CanPromote]
    else:
        raise InputError(f"Unknown action: {action}")
    categories = []
    print(permissions)
    for permission in permissions:
        categories.append((permission.category.name, permission.category.id))
    return render_template("select-category.html", categories=categories, action=action)


@app.route("/manage-category")
def manage_category():
    return select_category("modify")


@app.route("/members/<category>")
def members(category):
    raise NotImplementedError()
    return render_template("members.html")


def get_users_of_lower_level(user, category):
    permission = Permissions.query.filter_by(user=user, category=category).first()
    if permission is None:
        permission = create_permission(user, category)
    permissions = Permissions.query.filter_by(category=category).all()
    print("everything" + str(permissions))
    posts = category.posts
    users = [post.user for post in posts] + [p.user for p in permissions]
    print(users)
    return [poster for poster in users if
            Permissions.query.filter_by(user=poster, category=category).first().level > permission.level]


@app.route("/delete-category/<category_id>")
def delete_category(category_id):
    user_id = request.cookies.get('userID')
    if user_id is None:
        abort(401)
    user = User.query.filter_by(id=user_id).first()
    category = Category.query.filter_by(id=category_id).first()
    permission = Permissions.query.filter_by(user=user, category=category).first()
    if permission is None:
        permission = create_permission(user, category)
    users = get_users_of_lower_level(user, category)
    print(users, user, category, permission, sep="\n***")
    posts = [post for post in Post.query.filter_by(user=user).all() if category in post.category]
    if permission.canDelete:
        for poster in users:
            posts.extend([post for post in Post.query.filter_by(user=poster).all() if category in post.category])
    if user is not None:
        return render_template("remove-post.html", err=request.args.get('err'), category=category_id, posts=posts)
    else:
        return redirect(url_for("view_category",
                                err="You need to sign in to delete that post",
                                category_id=category_id),
                        code=302)


@app.route("/del-post", methods=["GET", "POST"])
def remove_post_to_category():
    if request.method == 'POST':
        post_id = request.form['post']
        post = Post.query.filter_by(id=post_id).first()
        cat_id = request.form['category']
        cat = Category.query.filter_by(id=cat_id).first()
        user_id = request.cookies.get('userID')
        user = User.query.filter_by(id=user_id).first()
        perms = Permissions.query.filter_by(user=user, category=cat).first()
        if perms is None:
            perms = create_permission(user, cat)
        if perms.canDelete and Permissions.query.filter_by(user=post.user, category=cat).first().level > perms.level \
                or post.user == user:
            print(f"adding post, {post.title}, to category, {cat.name}.")
            if post in cat.posts:
                cat.posts.remove(post)
                db.session.commit()
            else:
                return home(err="post is not in that category")
            return redirect(url_for("view_category", category_id=cat_id), code=302)
        else:
            return redirect(url_for("view_category",
                                    err="You do not have permission to delete that post",
                                    category_id=cat_id),
                            code=302)
    else:
        return redirect(url_for("home", code=302))


@app.route("/add_to_category/<category_id>")
def select_post(category_id):
    user_id = request.cookies.get('userID')
    if user_id is None:
        abort(401)
    user = User.query.filter_by(id=user_id).first()
    cat = Category.query.filter_by(id=category_id).first()
    permission = Permissions.query.filter_by(user=user, category=cat).first()
    if permission is None:
        permission = create_permission(user, cat)
    posts = Post.query.filter_by(user=user).all()
    posts = [post for post in posts if cat not in post.category]
    if user is not None and permission.canPost:
        return render_template("add-post.html", category=category_id, posts=posts)
    else:
        return redirect(url_for("view_category",
                                err="You do not have permission to add posts to this category",
                                category_id=category_id),
                        code=302)


@app.route("/timeout/<category_id>")
def timeout(category_id):
    user_id = request.cookies.get('userID')
    if user_id is None:
        abort(401)
    user = User.query.filter_by(id=user_id).first()
    category = Category.query.filter_by(id=category_id).first()
    permission = Permissions.query.filter_by(user=user, category=category).first()
    if permission is None:
        permission = create_permission(user, category)
    users = get_users_of_lower_level(user, category)
    if user is not None and permission.canTimeout:
        render_template("timeout.html", err=request.args.get('err'), category=category_id, users=users)
    else:
        return redirect(url_for("view_category",
                                err="You do not have permission to timeout in that category",
                                category_id=category_id),
                        code=302)


@app.route("/timeout-form", methods=["GET", "POST"])
def timeout_user():
    if request.method == 'POST':
        cat_id = request.form['cat_id']
        cat = Category.query.filter_by(id=cat_id).first()
        user_id = request.cookies.get('userID')
        user = User.query.filter_by(id=user_id).first()
        perms = Permissions.query.filter_by(user=user, category=cat).first()
        if perms is None:
            perms = create_permission(user, cat)
        username = request.form["username"]
        user_to_timeout = User.query.filter_by(name=username)
        user_timeout_perms = Permissions.query.filter_by(user=user_to_timeout, category=cat)
        time = request.form["time"]

        if perms.canTimeout and perms.level < user_timeout_perms.level:
            user_timeout_perms.canPost = False
            db.session.commit()
            return redirect(url_for("view_category", category_id=cat_id), code=302)
        else:
            return redirect(url_for("timeout",
                                    err="You do not have permission to timeout that person",
                                    category_id=cat_id),
                            code=302)
    else:
        return redirect(url_for("home", code=302))


@app.route("/mute/<category_id>")
def mute(category_id):
    user_id = request.cookies.get('userID')
    if user_id is None:
        abort(401)
    user = User.query.filter_by(id=user_id).first()
    category = Category.query.filter_by(id=category_id).first()
    permission = Permissions.query.filter_by(user=user, category=category).first()
    if permission is None:
        permission = create_permission(user, category)
    users = get_users_of_lower_level(user, category)
    if user is not None and permission.canMute:
        return render_template("mute.html", err=request.args.get('err'), category=category_id, users=users)
    else:
        return redirect(url_for("view_category",
                                err="You do not have permission to mute",
                                category_id=category_id),
                        code=302)


@app.route("/mute-form", methods=["GET", "POST"])
def mute_user():
    if request.method == 'POST':
        cat_id = request.form['category']
        cat = Category.query.filter_by(id=cat_id).first()
        user_id = request.cookies.get('userID')
        user = User.query.filter_by(id=user_id).first()
        perms = Permissions.query.filter_by(user=user, category=cat).first()
        if perms is None:
            perms = create_permission(user, cat)
        user_mute_id = request.form["user"]
        user_to_mute = User.query.filter_by(id=user_mute_id).first()
        user_mute_perms = Permissions.query.filter_by(user=user_to_mute, category=cat).first()

        if perms.canMute and perms.level < user_mute_perms.level:
            user_mute_perms.canPost = False
            db.session.commit()
            return redirect(url_for("view_category", category_id=cat_id), code=302)
        else:
            return redirect(url_for("mute",
                                    err="You do not have permission to mute that person",
                                    category_id=cat_id),
                            code=302)
    else:
        redirect(url_for("home"), code=302)


@app.route("/ban/<category_id>")
def ban(category_id):
    user_id = request.cookies.get('userID')
    if user_id is None:
        abort(401)
    user = User.query.filter_by(id=user_id).first()
    category = Category.query.filter_by(id=category_id).first()
    permission = Permissions.query.filter_by(user=user, category=category).first()
    if permission is None:
        permission = create_permission(user, category)
    users = get_users_of_lower_level(user, category)
    if user is not None and permission.canBan:
        return render_template("ban.html", err=request.args.get('err'), category=category_id, users=users)
    else:
        return redirect(url_for("view_category",
                                err="You do not have permission to ban in that category",
                                category_id=category_id),
                        code=302)


@app.route("/ban-form", methods=["GET", "POST"])
def ban_user():
    if request.method == 'POST':
        cat_id = request.form['category']
        cat = Category.query.filter_by(id=cat_id).first()
        user_id = request.cookies.get('userID')
        user = User.query.filter_by(id=user_id).first()
        perms = Permissions.query.filter_by(user=user, category=cat).first()
        if perms is None:
            perms = create_permission(user, cat)
        user_ban_id = request.form["user"]
        user_to_ban = User.query.filter_by(id=user_ban_id).first()
        user_ban_perms = Permissions.query.filter_by(user=user_to_ban, category=cat).first()
        print(user_ban_id)

        if perms.canBan and perms.level < user_ban_perms.level:
            user_ban_perms.canPost = False
            user_ban_perms.canView = False
            db.session.commit()
            return redirect(url_for("view_category", category_id=cat_id), code=302)
        else:
            return redirect(url_for("ban",
                                    err="You do not have permission to ban that person",
                                    category_id=cat_id),
                            code=302)
    else:
        redirect(url_for("home"), code=302)


@app.route("/promote/<category_id>")
def promote(category_id):
    user_id = request.cookies.get('userID')
    if user_id is None:
        abort(401)
    user = User.query.filter_by(id=user_id).first()
    category = Category.query.filter_by(id=category_id).first()
    permission = Permissions.query.filter_by(user=user, category=category).first()
    if permission is None:
        permission = create_permission(user, category)
    users = get_users_of_lower_level(user, category)
    users_id = [poster.id for poster in users]
    if user is not None and permission.canPromote:
        return render_template("promote.html", err=request.args.get('err'), category=category_id, users=users, users_id=users_id)
    else:
        return redirect(url_for("view_category",
                                err="You do not have permission to promote in this category",
                                category_id=category_id),
                        code=302)


@app.route("/get-level/<category_id>/<user_promote_id>", methods=["GET", "POST"])
def getLevel(category_id, user_promote_id):
    if request.method == "GET":
        user_id = request.cookies.get('userID')
        if user_id is None:
            abort(401)
        user = User.query.filter_by(id=user_id).first()
        category = Category.query.filter_by(id=category_id).first()
        permission = Permissions.query.filter_by(user=user, category=category).first()
        if permission is None:
            permission = create_permission(user, category)
        user_to_promote = User.query.filter_by(id=user_promote_id).first()
        user_promote_permission = Permissions.query.filter_by(user=user_to_promote, category=category).first()
        if user is not None and permission.canPromote:
            return str(user_promote_permission.level)
        else:
            return "is not available for this user."
    else:
        redirect(url_for("home"), code=302)
        
@app.route("/get-level/<category_id>/")
def noUser(category_id):
    return "is not available for this user."


@app.route("/promote-form", methods=["GET", "POST"])
def promote_user():
    if request.method == 'POST':
        cat_id = request.form['category']
        cat = Category.query.filter_by(id=cat_id).first()
        user_id = request.cookies.get('userID')
        user = User.query.filter_by(id=user_id).first()
        perms = Permissions.query.filter_by(user=user, category=cat).first()
        new_level = request.form['level']
        if perms is None:
            perms = create_permission(user, cat)
        promoteID = request.form["user"]
        user_to_promote = User.query.filter_by(id=promoteID).first()
        user_promote_perms = Permissions.query.filter_by(user=user_to_promote, category=cat).first()
        if user_promote_perms is None:
            user_promote_perms = create_permission(user, cat)
        if not new_level.isdigit():
            return redirect(url_for("promote",
                                    err="%s is not a valid number" % (new_level),
                                    category_id=cat_id),
                            code=302)
        
        if perms.canPromote and perms.level + 1 < user_promote_perms.level and perms.level + 1 < int(new_level):
            user_promote_perms.level = int(new_level)
            db.session.commit()
            print(new_level)
            return redirect(url_for("view_category",
                                    msg="You have successfully promoted %s to level %s" % (user_to_promote.username, user_promote_perms.level),
                                    category_id=cat_id),
                            code=302)
        else:
            return redirect(url_for("promote",
                                    err="You do not have permission to promote that person",
                                    category_id=cat_id),
                            code=302)
    else:
        redirect(url_for("home"), code=302)


@app.route("/modify/<category_id>")
def modify(category_id):
    actions = []
    user_id = request.cookies.get('userID')
    if user_id is None:
        abort(401)
    user = User.query.filter_by(id=user_id).first()
    category = Category.query.filter_by(id=category_id).first()
    permission = Permissions.query.filter_by(user=user, category=category).first()
    if permission is None:
        permission = create_permission(user, category)
    if permission.canView:
        actions.append("view")
    if permission.canPost:
        actions.append("post")
    if permission.canDelete:
        actions.append("delete")
    if permission.canTimeout:
        pass
    if permission.canMute:
        actions.append("mute")
    if permission.canBan:
        actions.append("ban")
    if permission.canPromote:
        actions.append("promote")
    if permission.canPromote:
        actions.append("modify roles")
    if permission.canInvite:
        actions.append("invite")
    if user is not None:
        return render_template('modify.html', actions=actions, category_id=category_id, category_name=category.name)
    else:
        redirect(url_for("home", msg="You need to sign in to access categories"), code=302)


@app.route("/roles/<category_id>")
def roles(category_id):
    user_id = request.cookies.get('userID')
    if user_id is None:
        abort(401)
    user = User.query.filter_by(id=user_id).first()
    category = Category.query.filter_by(id=category_id).first()
    permission = Permissions.query.filter_by(user=user, category=category).first()
    if permission is None:
        permission = create_permission(user, category)
    users = get_users_of_lower_level(user, category)
    users_id = [poster.id for poster in users]
    if user is not None and permission.canPromote:
        return render_template("roles.html", err=request.args.get('err'), category=category_id, users=users, users_id=users_id, perms=permission)
    else:
        return redirect(url_for("view_category",
                                err="You do not have permission to modify roles in that category",
                                category_id=category_id),
                        code=302)


@app.route("/get-roles/<category_id>/<changed_user_id>/<role_name>", methods=["GET", "POST"])
def get_roles(category_id, changed_user_id, role_name):
    if request.method == 'GET':
        cat = Category.query.filter_by(id=category_id).first()
        user_id = request.cookies.get('userID')
        user = User.query.filter_by(id=user_id).first()
        perms = Permissions.query.filter_by(user=user, category=cat).first()
        if perms is None:
            perms = create_permission(user, cat)
        user_to_change_roles = User.query.filter_by(id=changed_user_id).first()
        user_change_perms = Permissions.query.filter_by(user=user_to_change_roles, category=cat).first()

        if perms.canPromote and perms.level < user_change_perms.level:
            if role_name in user_change_perms.__dir__():
                return str(user_change_perms.__getattribute__(role_name))
            return "No permission by that name. Please check the spelling."
        else:
            return "Unauthorised for this access"
    else:
        redirect(url_for("home"), code=302)
    


@app.route("/change-role", methods=["GET", "POST"])
def change_role():
    if request.method == 'POST':
        cat_id = request.form['category']
        cat = Category.query.filter_by(id=cat_id).first()
        user_id = request.cookies.get('userID')
        user = User.query.filter_by(id=user_id).first()
        perms = Permissions.query.filter_by(user=user, category=cat).first()
        if perms is None:
            perms = create_permission(user, cat)
        changed_userID = request.form["user"]
        user_to_change_roles = User.query.filter_by(id=changed_userID).first()
        user_change_perms = Permissions.query.filter_by(user=user_to_change_roles, category=cat).first()

        if perms.canPromote and perms.level < user_change_perms.level:
            user_change_perms.canPost = request.form.get("post") == "true" and perms.canPost
            user_change_perms.canDelete = request.form.get("delete") == "true" and perms.canDelete
            user_change_perms.canView = request.form.get("view") == "true" and perms.canView
            user_change_perms.canTimeout = request.form.get("timeout") == "true" and perms.canTimeout
            user_change_perms.canAttachFiles = request.form.get("files") == "true" and perms.canAttachFiles
            user_change_perms.canMute = request.form.get("mute") == "true" and perms.canMute
            user_change_perms.canBan = request.form.get("ban") == "true" and perms.canBan
            user_change_perms.canPromote = request.form.get("promote") == "true" and perms.canPromote
            user_change_perms.canInvite = request.form.get("invite") == "true" and perms.canInvite
            db.session.commit()
            return redirect(url_for("view_category", category_id=cat_id), code=302)
        else:
            return redirect(url_for("roles",
                                    err="You do not have permission to promote that person",
                                    category_id=cat_id),
                            code=302)
    else:
        redirect(url_for("home"), code=302)


@app.route("/invite/<category_id>")
def invite(category_id):
    user_id = request.cookies.get('userID')
    if user_id is None:
        abort(401)
    user = User.query.filter_by(id=user_id).first()
    category = Category.query.filter_by(id=category_id).first()
    permission = Permissions.query.filter_by(user=user, category=category).first()
    if permission is None:
        permission = create_permission(user, category)
    if user is not None and permission.canPromote:
        return render_template("invite.html", err=request.args.get('err'), category=category_id)
    else:
        return redirect(url_for("view_category",
                                err="You do not have permission to modify roles",
                                category_id=category_id),
                        code=302)


@app.route("/invite-user", methods=["GET", "POST"])
def invite_user():
    if request.method == 'POST':
        cat_id = request.form['category']
        cat = Category.query.filter_by(id=cat_id).first()
        user_id = request.cookies.get('userID')
        user = User.query.filter_by(id=user_id).first()
        perms = Permissions.query.filter_by(user=user, category=cat).first()
        post = request.form.get("post")
        view = request.form.get("view")
        embed = request.form.get("embed")
        if perms is None:
            perms = create_permission(user, cat)
        invitee = User.query.filter_by(username=request.form['name']).all()
        if not invitee:
            return redirect(url_for("invite",
                                    err="No one by that username found",
                                    category_id=cat_id),
                            code=302)
        elif len(invitee) > 1:
            return redirect(url_for("invite", err="multiple users by that username found", category_id=cat_id),
                            code=302)
        else:
            invitee = invitee[0]
        invitee_perms = Permissions.query.filter_by(user_id=invitee.id, category_id=cat.id).first()
        if invitee_perms is None:
            invitee_perms = create_permission(invitee, cat)
        if perms.canInvite and perms.canView and perms.canPost:
            invitee_perms.canPost = (post == "true" and perms.canPost) or invitee_perms.canPost
            invitee_perms.canView = (view == "true" and perms.canView) or invitee_perms.canView
            invitee_perms.canAttachFiles = (embed == "true" and perms.canAttachFiles) or invitee_perms.canAttachFiles
            db.session.commit()
            return redirect(url_for("view_category", category_id=cat_id), code=302)
        else:
            redirect(url_for("view_category",
                             err="You do not have permission to promote that person",
                             category_id=cat_id),
                     code=302)
    else:
        redirect(url_for("home"), code=302)


@app.route("/category-action/<cat_id>/<action>")
def run_action(action, cat_id):
    print(request.environ["HTTP_HOST"])
    if action == "view":
        return redirect(url_for("view_category", category_id=cat_id), code=302)
    elif action == "post":
        return redirect(url_for("select_post", category_id=cat_id), code=302)
    elif action == "delete":
        return redirect(url_for("delete_category", category_id=cat_id), code=302)
    elif action == "timeout":
        pass
    elif action == "mute":
        return redirect(url_for("mute", category_id=cat_id), code=302)
    elif action == "ban":
        return redirect(url_for("ban", category_id=cat_id), code=302)
    elif action == "promote":
        return redirect(url_for("promote", category_id=cat_id), code=302)
    elif action == "modify":
        return redirect(url_for("modify", category_id=cat_id), code=302)
    elif action == "modify roles":
        return redirect(url_for("roles", category_id=cat_id), code=302)
    elif action == "invite":
        return redirect(url_for("invite", category_id=cat_id), code=302)
    elif action == "request access":
        pass
    else:
        raise InputError(f"Unknown action: {action}")
    raise NotImplementedError(f"Unimplemented action: {action}")


@app.route("/follow/<category_id>")
def follow(category_id):
    category = Category.query.filter_by(id=category_id).first()
    user_id = request.cookies.get('userID')
    user = User.query.filter_by(id=user_id).first()
    perms = Permissions.query.filter_by(user=user, category=category).first()
    if perms is None:
        perms = create_permission(user, category)
    print(perms.followed)
    perms.followed = True
    db.session.commit()
    print(perms.followed)
    return render_template('blank.html')


@app.route("/unfollow/<category_id>")
def unfollow(category_id):
    category = Category.query.filter_by(id=category_id).first()
    user_id = request.cookies.get('userID')
    user = User.query.filter_by(id=user_id).first()
    perms = Permissions.query.filter_by(user=user, category=category).first()
    if perms is None:
        perms = create_permission(user, category)
    print(perms.followed)
    perms.followed = False
    db.session.commit()
    print(perms.followed)
    return render_template('blank.html')


if __name__ == "__main__":
    if 'PORT' in os.environ:
        port = os.environ['PORT']
    else:
        port = 5000
    app.run(debug=True, host="0.0.0.0", port=int(port))
