from flask import Flask, jsonify
from app.blueprints.web import web
from app.blueprints.api import api

app = Flask(__name__)

app.register_blueprint(web, url_prefix='/')
app.register_blueprint(api, url_prefix='/api')

@app.errorhandler(404)
def not_found(error):
  return jsonify({}), 404

@app.errorhandler(403)
def forbidden(error):
  return jsonify({}), 403

@app.errorhandler(400)
def bad_request(error):
  return jsonify({}), 400

@app.errorhandler(Exception)
def handle_error(error):
  message = error.description if hasattr(error, 'description') else [str(x) for x in error.args]
  response = {
    'error': {
      'type': error.__class__.__name__,
      'message': message
    }
  }

  return response, error.code if hasattr(error, 'code') else 500