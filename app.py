
from flask import Flask
from views import IndexView, PredictDigitView
from settings import CLASSIFIER_STORAGE
from repo import ClassifierRepo
from services import PredictDigitService
from flask import Flask, render_template

from flask import Flask, render_template, request, Response, jsonify

import os

app = Flask(__name__)

# Route for the index page
@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = request.json.get('image')
    print('Received image URL:', image_url)
    if request.method == 'POST':
        try:
            image_url = request.form.get('image_url')

            # Create an instance of the ClassifierRepo
            repo = ClassifierRepo(CLASSIFIER_STORAGE)
            
            # Create an instance of the PredictDigitService
            service = PredictDigitService(repo)

            # Make the prediction using the image URL
            prediction = service.handle(image_url)

            # Return the prediction in a JSON response
            return jsonify({'prediction': prediction})
        
        except Exception as e:
            # Return an error message in a JSON response
            return jsonify({'error': str(e)}), 500

    # Handle the GET request
    return render_template('index.html')


# Register the views
app.add_url_rule('/', view_func=IndexView.as_view('index'), methods=['GET'])
app.add_url_rule('/api/predict', view_func=PredictDigitView.as_view('predict_digit'), methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)






