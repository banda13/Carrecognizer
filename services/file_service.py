from flask import Flask, render_template, request, Blueprint
from werkzeug.utils import secure_filename

file_upload = Blueprint('upload', __name__)
file_uploader = Blueprint('uploader', __name__)


@file_upload.route('/upload')
def upload_file():
    return render_template('upload.html')


@file_uploader.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save("uploads/" + secure_filename(f.filename))
        return 'file uploaded successfully'
