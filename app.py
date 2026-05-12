from flask import Flask, render_template
from extensions import db, login_manager
from routes.auth import auth
from routes.morse import morse
from routes.todolist import todolist
from routes.friends import friends
from models import User
from dotenv import load_dotenv
import os
from flask_migrate import Migrate






load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(auth)
app.register_blueprint(morse)
app.register_blueprint(todolist)
app.register_blueprint(friends)

login_manager.init_app(app)
login_manager.login_view = "auth.login"


projects = [
    {"name": "Friends", "endpoint": "friends.index"},
    {"name": "To-Do List", "endpoint": "todolist.index"},
    {"name": "Morse Converter", "endpoint": "morse.index"},
]

# Inject into ALL templates automatically
@app.context_processor
def inject_projects():
    return {"projects": projects}

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
