from flask import Blueprint, request, make_response, jsonify, abort
from app.database.user import register_user, login_user
from app.database.logs import add_log, view_logs
from base64 import b64encode, b64decode
import json

api = Blueprint('api', __name__)


@api.before_request
def log():
  add_log('api', request.remote_addr, request.path, request.headers.get('User-Agent'))

@api.route('/login', methods=['POST'])
def login():
  data = request.get_json()

  username = data.get('name')
  password = data.get('pass')

  user = login_user(username, password)
  if user is None:
    return jsonify({
      "error": True,
      "reason": "incorrect password."
    })

  b64 = b64encode(json.dumps(user).encode()).decode()
  
  toret = {"error": False, "user": user }

  res = jsonify(toret)
  res.set_cookie('auth', b64)
  
  return res

@api.route('/health', methods=['GET'])
def health():
  return jsonify({'error': False, 'health': 'OK'})

@api.route('/register', methods=['POST'])
def register():
  data = request.get_json()

  username = data.get('name')
  password = data.get('pass')

  user = register_user(username, password)
  if user is None:
     return jsonify({
      "error": True,
      "reason": "error while creating user."
    })
  toret = {"error": False, "user": user }
  return jsonify(toret)

@api.route('/admin/logs', methods=['GET'])
def logs():
  logs = view_logs()
  return jsonify(logs)