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
        
        image_processor = process_image(image_data_uri)
        x = image_processor.process_image()  # Update this line with the appropriate method for image processing
        if x is None:
            return 0

        prediction = classifier.predict(x)[0]
        return prediction
