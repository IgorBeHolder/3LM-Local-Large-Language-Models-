@app.route("/manage-model", methods=["POST"])
def manage_model():
    action = request.form.get("action")
    selected_models = request.form.getlist("selected_model")

    if action == "Delete":
        # ... deletion logic ...

    elif action == "Activate":
        model_id = selected_models[0]  # assuming only one model can be activated at once
        model = MLModel.query.get(int(model_id))
        if model:
            # Here, let's say the 'load_ml_model' function loads your ML model from its path
            # load_ml_model(model.path)

            # Store the model's name in the session
            session['active_model'] = model.name
            flash(f"Model {model.name} has been activated.", "success")

    return redirect(url_for('models.load_model'))

@app.context_processor
def inject_active_model():
    return {'active_model': session.get('active_model')}