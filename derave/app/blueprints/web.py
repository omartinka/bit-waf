from flask import Blueprint, render_template, request
from base64 import b64encode, b64decode
from app.database.logs import add_log
import json

web = Blueprint('web', __name__)

@web.before_request
def log():
  add_log('web', request.remote_addr, request.path, request.headers.get('User-Agent'))

@web.route('/', methods=['GET'])
def index():
  auth = request.cookies.get('auth')
  if auth == None:
    return render_template('login.html')

  user = json.loads(b64decode(auth).decode())
  if user['privileges'] == 1:
    return render_template('admin.html')

  return render_template('index.html')

@web.route('/login', methods=['GET'])
def login():
  return render_template('login.html')