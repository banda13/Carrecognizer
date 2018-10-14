#!flask/bin/python
from flask import Flask, Blueprint

test_service = Blueprint('test', __name__)

@test_service.route('/')
def index():
    return "Hello, World!"