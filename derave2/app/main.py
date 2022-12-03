from flask import Flask, jsonify
from app.blueprints.web import web

app = Flask(__name__)

app.register_blueprint(web, url_prefix='/')

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
  return jsonify({}), 500