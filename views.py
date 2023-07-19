from flask import render_template, request, Response
from flask.views import MethodView, View

from flask.views import View

from repo import ClassifierRepo
from services import PredictDigitService
from settings import CLASSIFIER_STORAGE

from flask import Flask, render_template, request, Response, jsonify

class IndexView(MethodView):
    def get(self):
        return render_template('index.html')

class PredictDigitView(MethodView):
    def post(self):
        if request.is_json:
            try:
                image_url = request.json.get('image')
                if not image_url:
                    return jsonify({'error': 'Invalid image URL.'}), 400

                # Create an instance of the ClassifierRepo
                repo = ClassifierRepo(CLASSIFIER_STORAGE)

                # Create an instance of the PredictDigitService
                service = PredictDigitService(repo)

                # Create an instance of the ProcessImage
                image_processor = ProcessImage(image_url)

                # Process the image
                image_data = image_processor.process_image()
                if image_data is None:
                    return jsonify({'error': 'Error processing image.'}), 400

                # Make the prediction
                prediction = service.handle(image_data)

                # Return the prediction in a JSON response
                return jsonify({'prediction': prediction})

            except Exception as e:
                # Return an error message in a JSON response
                return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': 'Invalid request. Expected JSON data.'}), 400