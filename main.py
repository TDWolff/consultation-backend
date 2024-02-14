import threading

# import "packages" from flask
from flask import render_template,request  # import render_template from "public" flask libraries
from flask.cli import AppGroup
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Message
from flask_mail import Mail
from migrate import initHouses, initImages


# import "packages" from "this" project
from __init__ import app, db, cors  # Definitions initialization


# setup APIs
from api.user import user_api # Blueprint import api definition
from api.player import player_api
from api.searchstocks import search_api
from api.house import house_api
# database migrations
from model.users import initUsers
from model.players import initPlayers

# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'torindeanwolff@gmail.com'
app.config['MAIL_PASSWORD'] = 'dslo bpmz hzwv tvnn'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)


# register URIs
app.register_blueprint(user_api) # register api routes
app.register_blueprint(player_api)
app.register_blueprint(app_projects) # register app pages
app.register_blueprint(search_api)
app.register_blueprint(house_api)

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/403/')
def error():
    return render_template('403.html'), 403

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/aws/')  # connects /about/ URL to about() function
def aws():
    return render_template("aws.html")

@app.route('/house/')
def house():
    return render_template("houses.html")

@app.route('/house/house-details/')
def housedetails():
    return render_template("housedetails.html")

@app.route('/house/edit-house/')
def edithouse():
    return render_template("edit-house.html")

@app.route('/table/')  # connects /stub/ URL to stub() function
def table():
    return render_template("table.html")

@app.route('/search/')
def search():
    return render_template("stocksearch.html")

@app.route('/register/', methods=['GET', 'POST'])
def register():
    # Define your site variable here
    site = {'baseurl': 'http://localhost:8086'}

    if request.method == 'POST':
        uid = request.form.get('uid')
        password = request.form.get('password')
        name = request.form.get('name')
        pnum = request.form.get('pnum')
        print(f"uid: {uid}, password: {password}, name: {name}, pnum: {pnum})")

        if not (uid and password and name and pnum):
            flash('Please fill out all fields.')
            return redirect(url_for('register'))

@app.route('/signin/', methods=['GET', 'POST'])
def signin():
    # Define your site variable here
    site = {'baseurl': 'http://localhost:8086'}
    return render_template('signin.html', site=site)

@app.route('/help/', methods=['GET', 'POST'])
def help():
    # Define your site variable here
    site = {'baseurl': 'http://localhost:8086'}
    return render_template('help.html', site=site)

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    # Define your site variable here
    site = {'baseurl': 'http://localhost:8086'}
    return render_template('logout.html', site=site)

@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    # Define your site variable here
    site = {'baseurl': 'http://localhost:8086'}
    return render_template('profile.html', site=site)

@app.route('/display/', methods=['GET'])
def display():
    site = {'baseurl': 'http://localhost:8086'}
    return render_template('getusers.html', site=site)


# @app.route('/display/')
# def display():
#     return render_template("displayusers.html")

@app.before_request
def before_request():
    # Check if the request came from a specific origin
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://localhost:8090']:
        cors._origins = allowed_origin

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8090')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to generate data
@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initPlayers()



# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)
        
# this runs the application on the development server
if __name__ == "__main__":
    # change name for testing
    app.run(debug=True, host="0.0.0.0", port="8086")
