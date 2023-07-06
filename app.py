import os

from flask import render_template, request, Response
from flask.views import MethodView, View

from flask.views import View

from repo import ClassifierRepo           
from services import PredictDigitService
from settings import CLASSIFIER_STORAGE

from sklearn.datasets import load_digits

from classifier import ClassifierFactory
from image_processing import process_image

app = Flask(__name__)

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

if __name__ == 'ML':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)



