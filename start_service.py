#!flask/bin/python
import os
from flask import Flask

from services.file_service import file_upload, file_uploader
from services.test_service import test_service

app = Flask(__name__)

app.register_blueprint(test_service, url_prefix='/test')
app.register_blueprint(file_upload, url_prefix='/file')
app.register_blueprint(file_uploader, url_prefix='/file')

port = int(os.environ.get("PORT", 5000))

app.run(host='0.0.0.0', port=port)