from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import os
from datetime import datetime
from dotenv import load_dotenv
from datetime import datetime
from routes.users import users
from routes.models import models
from routes.database import db, User, MLModel



load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")  # or "your_fallback_secret_key_here"

uri = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # silence the deprecation warning
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(models, url_prefix='/models')




# login_manager.init_app(app)
# Flask-Login configurations:
login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize Flask-Migrate after the db and app have been created
migrate = Migrate(app, db)


# Register the Blueprint
# app.register_blueprint(users)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        # You can pass the user_input to your model or LLM for a response.
        model_response = "You said: " + user_input
        return jsonify({"user_input": user_input, "model_response": model_response})
    return render_template("chat.html")


@app.route("/get-embeddings", methods=["POST"])
def get_embeddings():
    text = request.json["text"]
    embeddings = 'Embeddings for "{}"'.format(text)
    return render_template("get_embeddings.html", embeddings=embeddings)


@app.route("/upload-csv", methods=["GET", "POST"])
def upload_csv():
    if request.method == "POST":
        csv_file = request.files["csv_file"]
        if csv_file.filename.endswith(".csv"):
            file_path = os.path.join("uploads", csv_file.filename)
            csv_file.save(file_path)
            flash("CSV uploaded successfully!", "success")
        else:
            flash("Please upload a valid CSV file.", "danger")
        return redirect(
            url_for("upload_csv")
        )  # Ensure redirection after a POST request

    # List uploaded CSV files
    csv_files = []
    upload_dir = os.path.join(os.getcwd(), "uploads")
    for csv in os.listdir(upload_dir):
        csv_files.append(
            {
                "name": csv,
                "uploaded_on": datetime.fromtimestamp(
                    os.path.getctime(os.path.join(upload_dir, csv))
                ).strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return render_template("upload_csv.html", csv_files=csv_files)


@app.route("/manage-csv", methods=["POST"])
def manage_csv():
    # List uploaded CSV files
    csv_files = []
    upload_dir = os.path.join(os.getcwd(), "uploads")
    for csv in os.listdir(upload_dir):
        csv_files.append(
            {
                "name": csv,
                "uploaded_on": datetime.fromtimestamp(
                    os.path.getctime(os.path.join(upload_dir, csv))
                ).strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    selected_csvs = request.form.getlist("selected_csv")
    action = request.form.get("action")

    if action == "Delete":
        for csv in selected_csvs:
            os.remove(os.path.join("uploads", csv))
        flash(f"Deleted {len(selected_csvs)} CSV file(s) successfully!", "success")
        return redirect(url_for("upload_csv"))

    return render_template("upload_csv.html", csv_files=csv_files)


@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # In case of any database errors
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
