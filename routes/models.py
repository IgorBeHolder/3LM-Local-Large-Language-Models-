import os
from flask import Blueprint, session, render_template, redirect, url_for, request, flash
from routes.database import db, MLModel


models = Blueprint("models", __name__)


@models.route("/load-model", methods=["GET", "POST"])
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
        new_model = MLModel(
            name=model_file.filename, path=model_file_path
        )  # add any other necessary fields
        db.session.add(new_model)
        db.session.commit()

        uploaded_models = MLModel.query.all()

        # Flash a success message
        flash("Model uploaded successfully to {}!".format(selected_catalog), "success")

        # return redirect(url_for(""))

        # Redirect to the load_model route
    uploaded_models = MLModel.query.all()
    return render_template("load_model.html", models=uploaded_models)


@models.route("/manage-model", methods=["POST"])
def manage_model():
    action = request.form.get("action")
    selected_models = request.form.getlist("selected_model")

    if action == "Delete":
        for model_id in selected_models:
            model = MLModel.query.get(int(model_id))
            if model:
                db.session.delete(model)
                # Also delete the file from the file system if you want
                if os.path.exists(model.path):
                   os.remove(model.path)

        db.session.commit()
        flash("Selected models have been deleted.", "success")
        session["active_model"] = 'No model selected '

    elif action == "Activate":
        # check if a model is selected
        if len(selected_models) != 0:
            model_id = selected_models[
                0
            ]  # assuming only one model can be activated at once
            model = MLModel.query.get(int(model_id))
            # For the sake of this example, let's just print out the selected models.
            if model:
                # Here, let's say the 'load_ml_model' function loads your ML model from its path
                # load_ml_model(model.path)

                # Store the model's name in the session
                session["active_model"] = model.name
                flash(f"Model {model.name} has been activated.", "success")



    return redirect(url_for("models.load_model"))


@models.context_processor
def inject_active_model():
    """Injects the active model's name into the Jinja template"""
    return {"active_model": session.get("active_model")}
