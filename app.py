import os

from flask import Flask
from views import PredictDigitView, IndexView

app = Flask(__name__)