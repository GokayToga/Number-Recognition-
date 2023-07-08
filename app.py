
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
    if request.method == 'POST':
        # Get the image URL from the form submission
        image_url = request.form.get('image_url')
        
        # Validate the URL or perform any necessary checks
        
        # Create an instance of the PredictDigitService
        service = PredictDigitService()
        
        # Process the image and get the prediction
        prediction = service.handle(image_url)
        
        # Return the prediction as JSON response
        return jsonify({'prediction': prediction})
    
    # If it's a GET request, render the index template
    return render_template('index.html')

"""
app.add_url_rule(
    '/api/predict',
    view_func=PredictDigitView.as_view('predict_digit'),
    methods=['POST']
)

app.add_url_rule(
    '/',
    view_func=IndexView.as_view('index'),
    methods=['GET']
)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 4000))
    app.run(host='0.0.0.0', port=port)
"""
if __name__ == '__main__':
    app.run()



