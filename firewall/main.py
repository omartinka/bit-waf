import sys

def print_help():
  print('Usage: python main.py [args]')
  print('  --xss <name>  : specifies model for xss checking, in ./data folder')
  print('  --sqli <name> : specifies model for sqli checking, in ./data folder')
  print('  --train       : trains the model on startup. takes a few seconds.')
  print('  --help        : displays help and exits')

if '--help' in sys.argv or '-h' in sys.argv:
  print_help()
  exit(0)

from flask import Flask, request, Response, render_template, jsonify
from management.config import *
from management.proxy import proxy
import requests
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static_fw')
CORS(app)

@app.before_request
def before_req():
  print(request.host)
  if request.host.split(':')[0] != 'api.fw-management.local':
    return proxy(request, None)
  else:
    print('else proclo')

@app.route('/load', methods=['POST'])
def load():
  conf = request.get_json()
  set_ruleset(conf)
  return jsonify({"status": "ok"})

@app.route('/rules', methods=['GET'])
def get_config(): 
  return jsonify(get_ruleset())

PORT = 8080
HOST = '127.0.0.1'

app.run(host=HOST, port=PORT, debug=True, use_evalex=False)
