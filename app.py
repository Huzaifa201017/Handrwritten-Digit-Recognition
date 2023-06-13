from flask import Flask, request, jsonify,render_template
from werkzeug.utils import secure_filename
import os
from my_neural_network  import neuralNetwork 

app = Flask(__name__)

# Configuration for file upload
app.config['UPLOAD_FOLDER'] = 'uploads/'

n = neuralNetwork()
n.loadWeights()

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/index', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'no file'}), 400
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    prediction = int(n.predict_number(file_path))

    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    if not os.path.exists('uploads/'):
        os.makedirs('uploads/')
    app.run(debug=True)

