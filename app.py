import os

from flask import Flask
from views import PredictDigitView, IndexView

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


from flask import render_template, request, Response
from flask.views import MethodView, View

from flask.views import View

from repo import ClassifierRepo
from services import PredictDigitService
from settings import CLASSIFIER_STORAGE

class IndexView(View):
    def dispatch_request(self):
        return render_template('index.html')

class PredictDigitView(MethodView):
    def post(self):
        repo = ClassifierRepo(CLASSIFIER_STORAGE)
        service = PredictDigitService(repo)
        image_data_uri = request.json['image']
        prediction = service.handle(image_data_uri)
        return Response(str(prediction).encode(), status=200)
    
import os

BASE_DIR = os.getcwd()
CLASSIFIER_STORAGE = os.path.join(BASE_DIR, 'storage/classifier.txt')

import pickle

class ClassifierRepo:
    def __init__(self, storage):
        self.storage = storage

    def get(self):
        with open(self.storage, 'wb') as out:
            try:
                classifier_str = out.read()
                if classifier_str != '':
                    return pickle.loads(classifier_str)
                else:
                    return None
            except Exception:
                return None

    def update(self, classifier):
        with open(self.storage, 'wb') as in_:
            pickle.dump(classifier, in_)

from sklearn.datasets import load_digits

from classifier import ClassifierFactory
from image_processing import process_image

class PredictDigitService:
    def __init__(self, repo):
        self.repo = repo

    def handle(self, image_data_uri):
        classifier = self.repo.get()
        if classifier is None:
            digits = load_digits()
            classifier = ClassifierFactory.create_with_fit(
                digits.data,
                digits.target
            )
            self.repo.update(classifier)
        
        x = process_image(image_data_uri)
        if x is None:
            return 0

        prediction = classifier.predict(x)[0]
        return prediction
    
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

class ClassifierFactory:
    @staticmethod
    def create_with_fit(data, target):
        model = KNeighborsClassifier(n_neighbors=3)
        model.fit(data, target)
        return model


import numpy as np
from skimage import exposure
import base64
from PIL import Image, ImageOps, ImageChops
from io import BytesIO

def replace_transparent_background(image):
    image_arr = np.array(image)

    if len(image_arr.shape) == 2:
        return image

    alpha1 = 0
    r2, g2, b2, alpha2 = 255, 255, 255, 255

    red, green, blue, alpha = image_arr[:, :, 0], image_arr[:, :, 1], image_arr[:, :, 2], image_arr[:, :, 3]
    mask = (alpha == alpha1)
    image_arr[:, :, :4][mask] = [r2, g2, b2, alpha2]

    return Image.fromarray(image_arr)

def trim_borders(image):
    bg = Image.new(image.mode, image.size, image.getpixel((0,0)))
    diff = ImageChops.difference(image, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)
    
    return image

def pad_image(image):
    return ImageOps.expand(image, border=30, fill='#fff')

def invert_colors(image):
    return ImageOps.invert(image)

def resize_image(image):
    return image.resize((8, 8), Image.LINEAR)