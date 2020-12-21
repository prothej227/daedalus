from flask import Flask, render_template, url_for, redirect, flash
from flask import send_from_directory, send_file
import os
from data import movies
from data import series
import json

import time
from datetime import datetime, date
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_admin.form import DatePickerWidget
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, request, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES, DOCUMENTS

#NGROK INTEGRATION
#from flask_ngrok import run_with_ngrok


app = Flask(__name__, static_folder='static')
#Ngrok Run
#run_with_ngrok(app)

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.getcwd() + '\\database\\flask.db'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = ("Sign in to access this page.")
login_manager.login_message_category = ("warning")
admin_users = ['darkbit601', 'admin', 'JRNL']

# FlaskTV Data
movies = movies()
series = series()

#FlaskServices Data
def write_json(data, filename='print_job.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

#Uploads
photos = UploadSet('photos', IMAGES)
docs = UploadSet('docs', ['pdf', 'docx', 'doc', 'txt', 'ppt', 'pptx', 'xls', 'xlsx', 'rtf', 'odt'])
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads/' + str(date.today().strftime("%b-%d-%Y")) + '/photos'
app.config['UPLOADED_DOCS_DEST'] = 'static/uploads/' + str(date.today().strftime("%b-%d-%Y")) + '/docs'
app.config
configure_uploads(app, (photos, docs))

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15), unique = True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(80))
    about = db.Column(db.Text)
    birthday = db.column(db.String(100))
    date_joined = db.Column(db.DateTime)   

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired(), Length(min = 4, max = 15)])
    password = PasswordField('Password', validators =[InputRequired(), Length(min = 4, max = 80)])
    remember = BooleanField('Remember Me?')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators = [InputRequired(), Email(message = 'invalid email'), Length(max = 60)])
    username = StringField('Username', validators = [InputRequired(), Length(min = 4, max = 15)])
    password = PasswordField('Password', validators =[InputRequired(), Length(min = 8, max = 80)]) 
    about = StringField('Tell someting about yourself: (Hobbies, Interests etc.)', validators = [InputRequired()]) 

class Blogpost(db.Model):
    blog_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
    
@app.route('/')
def index():
        if current_user.is_authenticated:
            return render_template('home.html', name = current_user.username, info_date = datetime.now(), page_title = str(current_user.username))
        else:
            return render_template('home.html', name = 'Guess', info_date = datetime.now(), page_title = "Welcome")      
@app.route('/flask.png')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                          'flask.png',mimetype='image/vnd.microsoft.icon')

@app.route('/about')
def about():
        return render_template('about.html', page_title = "About")

@app.route('/articles')
def articles():
        posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
        return render_template('articles.html', posts = posts, page_title = "Articles")
        
@app.route('/post/article/<string:id>/')
def article(id):
        post = Blogpost.query.filter_by(blog_id = id).one()
        return render_template('article.html', id = id, post = post, page_title = post.title)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember = form.remember.data)
                return redirect(request.args.get('next') or url_for('index'))
            else:
                flash('Error: Wrong username or password.', 'danger')
        else:
            flash('Error: User does not exist.', 'danger')
    return render_template('login.html', form = form, page_title = "Login")

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method = 'sha256')
        new_user = User(username = form.username.data, email = form.email.data, password = hashed_password, about = form.about.data, date_joined = datetime.now().date())
        db.session.add(new_user)
        db.session.commit()
        flash('New User has been created.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form = form, page_title = "Sign Up")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("FlaskApp: You have logout.", "success")
    return redirect(url_for('index'))

@app.route('/2048')
@login_required
def game2048():
    return render_template('2048-game.html', page_title = "2048")

@app.route('/pacman')
@login_required
def gamepacman():
    return render_template('pacman.html', page_title = "Pacman")

@app.route('/<path:path>')
@login_required
def serve_page(path):
    return send_from_directory('static', path)

@app.route('/video/watch_id=ABCDEF')
@login_required
def video_player():
    return render_template('video_player.html', page_title = "iWatch")

@app.route('/editor')
@login_required
def add():
    return render_template('editor.html', page_title = "Editor v1")

@app.route('/editor/edit/art_id/<string:blog_id>/')
@login_required
def edit(blog_id):
    blog_data = Blogpost.query.filter_by(blog_id=blog_id).first()
    return render_template('editor_edit.html', page_title = "Edit/Update Post", blog_data = blog_data)


@app.route('/addpost', methods = ["POST"])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    content = request.form['content']
    
    if request.form['author'] != "":
        author = request.form['author']
    else:
        author = current_user.username

    post = Blogpost(title = title, subtitle = subtitle, author = author, content = content, date_posted = datetime.now())
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('articles'))

@app.route('/editpost/id/<string:blog_id>/', methods = ["POST"])
def editpost(blog_id):
    title = request.form['title']
    subtitle = request.form['subtitle']
    content = request.form['content']
    author = current_user.username

    BlogUpdate = Blogpost.query.filter_by(blog_id = blog_id).first()
    BlogUpdate.title = title
    BlogUpdate.subtitle = subtitle
    BlogUpdate.content =  content
    db.session.commit()
    return redirect(url_for('article', id = blog_id))

@app.route('/profile/<string:url_name>/')
@login_required
def user_profile(url_name):
    url_name  = current_user.username
    user_data = User.query.filter_by(username=current_user.username).first()
    date_joined = str(current_user.date_joined.date().strftime('%b %d, %Y'))
    blog_entry = Blogpost.query.filter_by(author = current_user.username).all()
    return render_template('profile.html', name = current_user.username, email = current_user.email, id = current_user.id, about = current_user.about, date_joined = date_joined, blog_entry = blog_entry, page_title = "User Page")

@app.route('/user/<string:username>/')
def user_page(username):
    user_data = User.query.filter_by(username=username).first()
    date_joined = str(user_data.date_joined.date().strftime('%b %d, %Y'))
    blog_entry = Blogpost.query.filter_by(author = user_data.username).all()
    return render_template('user_page.html', name = user_data.username, email = user_data.email, id = user_data.id, about = user_data.about, date_joined = date_joined, blog_entry = blog_entry, page_title = user_data.username)

@app.route('/tv')
@login_required
def flasktv():
    return render_template('flasktv.html', page_title = "Watch", movie_list = movies, series_list = series)

@app.route('/tv/movie/watch_name=<string:title>/')
def watch(title):
    for movie in movies:
        if title == movie.get('title'):
            return render_template('watch.html', page_title = "Watch " + movie.get('title'), title = movie.get('title'), year = movie.get('year'), link = movie.get('link'), body= movie.get('body'))  
    return render_template('error.html', page_title = "Watch", movie_list = movies)

@app.route('/tv/series/watch_name=<string:title>/ep_num=<string:ep>/')
def watch_series(title, ep):
    for ele in series:
        if title == ele.get('title'):
            return render_template('watch.html', page_title = "Watch " + ele.get('title'), title = ele.get('title') + " - Episode " + str(ep)  , year = ele.get('year'), link = str(ele.get('locator')) + '/EP-' + str(ep) + '.mp4', body= ele.get('body'))
    return render_template('error.html', page_title = "Watch", movie_list = movies)    

@app.route('/get/movie/<string:title>/')
def downloadFile (title):
    path =  os.getcwd() + "\\static\\media\\videos\\movies\\"
    file = path + title + ".mp4"
    return send_file(file, as_attachment=True)

@app.route('/tv/series/ep_viewer/<string:title>/')
def ep_viewer (title):
    for ele in series:
        if title == ele.get('title'):
            body = ele.get('body')
            ep = ele.get('ep')
            return render_template('episode_viewer.html', page_title = title, title = title, body = body, ep = int(ep))

@app.route('/search', methods = ['POST'])
def search_user():
    if request.method == 'POST':
        username = request.form['searchbox']
        if username == "":
            return render_template('error.html', page_title = "User not found")  
    return redirect(url_for('search_results', username = username))

@app.route('/search_user/query/name/<string:username>') 
def search_results(username):
    results = User.query.filter(User.username.contains(username))
    return render_template('search.html', page_title = "Search results for " + username, username = username, results = results)

@app.route('/image_editor/photo/<string:filename>') 
def image_editor(filename):
    path = '/static/uploads/' + str(date.today().strftime("%b-%d-%Y")) + '/photos/' + str(filename)
    return render_template('image_editor.html', page_title = "Image Editor", path = path)

@app.route('/print/') 
def access_print():
    return render_template('fprint_gateway.html', page_title = "FlaskPrint - Gateway")   

@app.route('/print/submit', methods = ['POST']) 
def f_print_verify_customer_data():
    if request.method == "POST":
        access_token = request.form['token'] 
        name = request.form['name']
        opttype = request.form['opttype']
        size  = request.form['size']
        color = request.form['color']
        quality = request.form['quality']
    return redirect(url_for('flaskprint', token = access_token, name = name, opttype = opttype, size = size, color = color, quality = quality))

@app.route('/print/job/token=<string:token>?name=<string:name>?type=<string:opttype>?size=<string:size>?color=<string:color>?quality=<string:quality>') 
def flaskprint(token, name, opttype, size, color, quality):
    token_list = []
    verif_token_list = []
    with open('access_token.json') as f:
        token_json = json.load(f)
    with open('print_job.json') as q:
        verif_token = json.load(q)
    for ele in token_json['tokens']:
        token_list.append(ele['tkn'])
    for ele1 in verif_token['print_job']:
        verif_token_list.append(ele1['access_token'])

    if token in token_list and token not in verif_token_list:
        return render_template('fprint.html', token = token, page_title = "FlaskPrint", name = name, opttype = opttype, size = size, quality = quality, color = color, ft_images = str(IMAGES), ft_docs = ['pdf', 'docx', 'doc', 'txt', 'ppt', 'pptx', 'xls', 'xlsx', 'rtf', 'odt'])
    elif token in token_list and token in verif_token_list:
        flash("Error: Token already used! Please consider purchasing another one.", 'warning')        
    else:
        flash("Error: Invalid/Wrong Access Token", 'danger')
    return redirect(url_for('access_print'))  

@app.route('/upload/edit?=<string:edit>/pass_data/<string:name>/<string:token>/<string:opttype>/<string:size>/<string:color>/<string:quality>', methods=['GET', 'POST'])
def upload(edit, name, token, opttype, size, color, quality):
    new_data = {
        'name': name,
        'access_token': token,
        'type': opttype,
        'size': size,
        'color': color,
        'quality': quality,
        'date': str(date.today().strftime("%b-%d-%Y")),
        }
    if request.method == 'POST' and 'photo' in request.files and edit == "true":
        filename = photos.save(request.files['photo'])
        #Write to JSON FILE
        return redirect(url_for('image_editor', filename = filename))
    elif request.method == 'POST' and 'photo' in request.files and edit == "false":
        filename = photos.save(request.files['photo'])
        #Write to JSON FILE
        with open('print_job.json') as json_file: 
            data = json.load(json_file)
            j_data = data['print_job']
            new_data['filename'] = filename
            j_data.append(new_data)
        write_json(data)

        flash('Image/Photo Added to Print Queue', 'success')
    elif request.method == 'POST' and 'doc' in request.files and edit == "false":
        filename = docs.save(request.files['doc'])
        #Write to JSON FILE
        with open('print_job.json') as json_file: 
            data = json.load(json_file)
            j_data = data['print_job']
            new_data['filename'] = filename            
            j_data.append(new_data)
        write_json(data)
        flash('Document Added to Print Queue', 'success')
    elif request.method == 'POST' and not filename:
        flash("Error: File not supported", 'danger')
    return render_template('/msg/success.html', page_title = "Success!")

@app.route('/print/dashboard') 
@login_required
def fprint_dashboard():
    # List
    name = list()
    token = list()
    opttype = list()
    size = list()
    color = list()
    quality = list()
    date = list()
    filename = list()
    # Administrative Privileges
    if current_user.username in admin_users:
        admin = current_user.username
        with open('print_job.json') as f:
            data = json.load(f)
            for job in data['print_job']:
                name.append(job['name'])
                token.append(job['access_token'])
                opttype.append(job['type'])
                size.append(job['size'])
                color.append(job['color'])
                quality.append(job['quality'])                                 
                date.append(job['date'])
                filename.append(job['filename'])
        return render_template('flaskprint/dashboard.html', page_title = "FlaskPrint Dashboard", names = name, tokens = token, opttypes = opttype, sizes = size, color = color, quality = quality, dates = date, types = opttype, filename = filename, length = len(name))  
    else:
        return render_template('error.html', page_title = "Access Denied", msg = "Page requires administrative privileges")

@login_required
@app.route('/print/dashboard/tokens')
def dashboard_token():
    token = list()
    no = list()
    date = list()
    verif_token_dash = list()
    if current_user.username in admin_users:
        with open('access_token.json') as f:
            token_json = json.load(f)
            for ele in token_json['tokens']:
                token.append(ele['tkn'])
                no.append(ele['id'])
                date.append(ele['date'])
        with open('print_job.json') as q:
            k = json.load(q)
            for ele in k['print_job']:
                verif_token_dash.append(ele['access_token'])        
        return render_template('flaskprint/token_list.html', page_title = "FlaskPrint Dashboard", tokens = token, dates = date, ids = no, length = len(no), v_list = verif_token_dash)
    else:
        return render_template('error.html', page_title = "Access Denied", msg = "Page requires administrative privileges")
if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 8080)
