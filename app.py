from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load-model', methods=['GET', 'POST'])
def load_model():
    # Load the specified model
    return render_template('load_model.html')

@app.route('/inference', methods=['GET', 'POST'])
def inference():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            # Handle JSON data
            text = request.json['text']
        else:
            # Handle form data
            text = request.form['text']

        # Use the loaded model to make a prediction
        prediction = 'Prediction for "{}"'.format(text)

        # Return the prediction
        return render_template('inference.html', prediction=prediction)
    else:
        # Render the inference page
        return render_template('inference.html')

# @app.route('/inference', methods=['GET','POST'])
# def inference():
#     # Get the text from the request
#     text = request.json['text']

#     # Use the loaded model to make a prediction
#     prediction = 'Prediction for "{}"'.format(text)

#     # Return the prediction
#     return render_template('inference.html', prediction=prediction)

@app.route('/get-embeddings', methods=['POST'])
def get_embeddings():
    # Get the text from the request
    text = request.json['text']

    # Use the loaded model to get the embeddings
    embeddings = 'Embeddings for "{}"'.format(text)

    # Return the embeddings
    return render_template('get_embeddings.html', embeddings=embeddings)

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    # Get the uploaded file from the request
    file = request.files['file']

    # Process the CSV file
    return 'CSV file processed successfully'

if __name__ == '__main__':
    app.run(debug=True)