from flask import render_template, request, Response
from flask.views import MethodView, View

from flask.views import View

from repo import ClassifierRepo
from services import PredictDigitService
from settings import CLASSIFIER_STORAGE

from flask import Flask, render_template, request, Response, jsonify


class IndexView(View):
    def dispatch_request(self):
        return render_template('index.html')

class PredictDigitView(MethodView):
    def post(self):
        if request.is_json:
            repo = ClassifierRepo(CLASSIFIER_STORAGE)
            service = PredictDigitService(repo)
            image_data_uri = request.json.get('image')
            prediction = service.handle(image_data_uri)
            return jsonify({'prediction': prediction})
        else:
            return jsonify({'error': 'Invalid request. Expected JSON data.'}), 400