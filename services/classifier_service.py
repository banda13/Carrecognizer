from classifiers.cnn3 import Cnn3

from flask import Flask, render_template, request, Blueprint
from werkzeug.utils import secure_filename

classifier = Blueprint('classifier', __name__)


@classifier.route('/classify', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save("uploads/" + secure_filename(f.filename))
        cnn = Cnn3("89e6a1a5-8a29-4cee-acd2-5fcb6d889bc6")
        label = cnn.predict("uploads/" + secure_filename(f.filename), f.filename)
        return label