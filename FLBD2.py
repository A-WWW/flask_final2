import sqlite3
import os
from flask import Flask, render_template, request, g, flash, url_for, redirect
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required
from UserLogin import UserLogin

DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'ffgke864kplgkdf09g4j5kj40dfr4jt4ki'
USERNAME = 'admin'
PASSWORD = '1111'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'flsite.db')))

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

# create_db()
def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.route("/")
def index():
    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPostsAnonce())

dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/add_post", methods=["POST", "GET"])
def addPost():

    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'])
            if not res:
                flash('Error, no comment added', category='error')
            else:
                flash('Comment added', category='success')
        else:
            flash('Error, no comment added', category='error')

    return render_template('add_post.html', menu=dbase.getMenu(), title="Adding a comment")


# @app.route("/post/<alias>")
# @login_required
# def showPost(alias):
#     title, post = dbase.getPost(alias)
#     if not title:
#         abort(404)
#
#     return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)

@app.route("/post/<int:id_post>")
def showPost(id_post):

    title, post = dbase.getPost(id_post)
    if not title:
        abort(404)
    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('index'))

        flash("Login or password do not match")

    return render_template("login.html", menu=dbase.getMenu(), title="Authorization")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":

        if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
                and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['name'], request.form['email'], hash)
            if res:
                flash("Are you registered")
                return redirect(url_for('login'))
            else:
                flash("Error")
        else:
            flash("Data entry error", "Error")

    return render_template("register.html", menu=dbase.getMenu(), title="Registration")

if __name__ == "__main__":
    app.run(debug=True)