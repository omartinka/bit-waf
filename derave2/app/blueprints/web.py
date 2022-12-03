from flask import Blueprint, render_template, request
from base64 import b64encode, b64decode
import json

web = Blueprint('web', __name__)

@web.route('/', methods=['GET'])
def index():
  return render_template('index.html')
