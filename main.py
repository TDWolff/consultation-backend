# import "packages" from flask
from flask import render_template, request, redirect, url_for, flash
from flask.cli import AppGroup
from flask import Flask
from flask_cors import CORS

# import "packages" from "this" project
from __init__ import app, db  # Definitions initialization

# setup APIs
from api.user import user_api  # Blueprint import api definition
from api.player import player_api
from api.consultation import consultation_api

# database migrations
from model.users import initUsers
from model.players import initPlayers
# setup App pages
from projects.projects import app_projects  # Blueprint directory import projects definition

# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)

# Initialize CORS
cors = CORS(app, origins=['http://localhost:8083', 'http://127.0.0.1:8083', 'https://tdwolff.github.io'], supports_credentials=True, methods=["GET", "POST", "PUT", "DELETE", "SEARCH"])

# register URIs
app.register_blueprint(user_api)  # register api routes
app.register_blueprint(player_api)
app.register_blueprint(app_projects)  # register app pages
app.register_blueprint(consultation_api)

@app.errorhandler(404)  # catch for URL not found
def page_not_found(_):
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
    return render_template('signin.html')

@app.route('/help/', methods=['GET', 'POST'])
def help():
    return render_template('help.html')

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    return render_template('logout.html')

@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')

@app.route('/display/', methods=['GET'])
def display():
    return render_template('getusers.html')

@app.before_request
def before_request():
    # Check if the request came from a specific origin
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://localhost:8083', 'http://127.0.0.1:8083', 'https://tdwolff.github.io']:
        cors._origins = allowed_origin

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
    app.run(debug=True, host="0.0.0.0", port="8088")