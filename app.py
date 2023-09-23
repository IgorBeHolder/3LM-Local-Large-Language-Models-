from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") # or "your_fallback_secret_key_here"

uri = os.environ.get("DATABASE_URI")
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # silence the deprecation warning

db = SQLAlchemy(app)

# with app.app_context():
#     db.create_all()


# Initialize Flask-Migrate after the db and app have been created
migrate = Migrate(app, db)

# User model:
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), nullable=False, default="user")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Model for uploaded ML models:
class MLModel(db.Model):
    model_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    path = db.Column(db.String(120), nullable=False)
    uploaded_on = db.Column(db.DateTime, default=datetime.utcnow)

# Flask-Login configurations:
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("index"))
        flash("Invalid credentials!", "danger")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Signed up successfully!", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/")
def index():
    return render_template("index.html")


from flask import flash, redirect, url_for

@app.route("/load-model", methods=["GET", "POST"])
def load_model():
    if request.method == "POST":
        model_file = request.files["model_file"]
        selected_catalog = request.form["catalog"]
        
        # Ensure the chosen directory exists or create it
        if not os.path.exists(selected_catalog):
            os.makedirs(selected_catalog)
        
        # Save the file to the chosen directory
        model_file_path = os.path.join(selected_catalog, model_file.filename)
        model_file.save(model_file_path)

        # Add the new model's info to the database
        new_model = MLModel(name=model_file.filename, path=model_file_path)  # add any other necessary fields
        db.session.add(new_model)
        db.session.commit()

        uploaded_models = MLModel.query.all()

        # Flash a success message
        flash("Model uploaded successfully to {}!".format(selected_catalog), "success")
        
        return redirect(url_for('load_model'))
    
        # Redirect to the load_model route
    uploaded_models = MLModel.query.all()
    return render_template("load_model.html", models=uploaded_models)



@app.route("/delete-model/<int:model_id>")
def delete_model(model_id):
    # Get the model using model_id
    model = MLModel.query.get(model_id)
    if model:
        # Delete the model file from the filesystem
        if os.path.exists(model.path):
            os.remove(model.path)
        
        # Delete the model record from the database
        db.session.delete(model)
        db.session.commit()
        return redirect(url_for('load_model'))
    else:
        return "Model not found", 404

@app.route("/select-model/<int:model_id>")
def select_model(model_id):
    # Get the model using model_id
    model = MLModel.query.get(model_id)
    if model:
        # Provide functionality to select the model for some operation
        pass  # Implement what should happen when a model is selected
    else:
        return "Model not found", 404





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
            return redirect(url_for('upload_csv'))
        else:
            flash("Please upload a valid CSV file.", "danger")
    return render_template("upload_csv.html")

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # In case of any database errors
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
