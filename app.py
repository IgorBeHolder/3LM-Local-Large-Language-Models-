import os
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate

from routes.users import users
from routes.models import models
from routes.inference import chat, getembeddings, uploadcsv, managecsv
from routes.database import db, User

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")  # or "your_fallback_secret_key_here"

uri = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # silence the deprecation warning
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(models, url_prefix="/models")
app.register_blueprint(chat, url_prefix="/inference")
app.register_blueprint(getembeddings, url_prefix="/inference")
app.register_blueprint(uploadcsv, url_prefix="/inference")
app.register_blueprint(managecsv, url_prefix="/inference")


login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Initialize Flask-Migrate after the db and app have been created
migrate = Migrate(app, db)


@app.route("/")
def index():
    return render_template("index.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # In case of any database errors
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
