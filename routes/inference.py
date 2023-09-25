import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from routes.database import db, User, MLModel
from datetime import datetime

chat = Blueprint("chat", __name__)
getembeddings = Blueprint("getembeddings", __name__)
uploadcsv = Blueprint("upload_csv", __name__)
managecsv = Blueprint("manage_csv", __name__)


@chat.route("/chat", methods=["GET", "POST"])
def chats():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        # You can pass the user_input to your model or LLM for a response.
        model_response = "You said: " + user_input
        return jsonify({"user_input": user_input, "model_response": model_response})
    return render_template("chat.html")


@getembeddings.route("/getembeddings", methods=["POST"])
def get_embeddings():
    text = request.json["text"]
    embeddings = f'Embeddings for "{text}"'
    return render_template("get_embeddings.html", embeddings=embeddings)


@uploadcsv.route("/upload_csv", methods=["GET", "POST"])
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
            url_for("upload_csv.upload_csv")
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


@managecsv.route("/manage_csv", methods=["POST"])
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
        return redirect(url_for("upload_csv.upload_csv"))

    return render_template("upload_csv.html", csv_files=csv_files)
