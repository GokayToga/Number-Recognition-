from sklearn.datasets import load_digits

from classifier import ClassifierFactory
from image_processing import ProcessImage

class PredictDigitService:
    def __init__(self, repo):
        self.repo = repo

    def handle(self, image_data_uri):
        image_processor = ProcessImage(image_data_uri)

        classifier = self.repo.get()
        if classifier is None:
            digits = load_digits()
            classifier = ClassifierFactory.create_with_fit(
                digits.data,
                digits.target
            )
            self.repo.update(classifier)
        
        x = image_processor.decode_image_data_uri(image_data_uri)
        if x is None:
            return 0

        prediction = classifier.predict(x)[0]
        return prediction
