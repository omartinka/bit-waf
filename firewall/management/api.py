from management.config import ruleset, get_ruleset, set_ruleset
from flask import request

# POST - loads an JSON config from request data and saves it
def load(req):
  if req.method not in ['POST', 'OPTIONS']:
    return {}, 400
  conf = req.json()
  print(conf)

  set_ruleset(conf)

# GET - sends out current loaded config
def get_config(req):
  if req.method not in ['GET', 'OPTIONS']:
    return {}, 400
  
  return jsonify(get_ruleset())