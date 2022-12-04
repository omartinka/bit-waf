from management.config import *
from model.antixss import anti_xss
from model.antisqli import anti_sqli

from flask import render_template, Response, jsonify, request
import requests

def check_req(path, rules, to_check, direction):
  for rule in rules:
    # Get endpoint
    if path == rule['path']:
      # check all rules in endpoint
      for x in rule['rules']:
        if x['dir'] != direction:
          continue
        
        if x['type'] == 'xss':
          r = anti_xss.check(to_check)
          if r == False:
            print('[BLOCKED]:', to_check)
            return {
              "error": True, 
              "reason": "XSS detected."
            }
        elif x['type'] == 'sqli':
          r = anti_sqli.check(to_check)
          print('is ok?', r)
          if r == False:
            print('[BLOCKED]:', to_check)
            return {
              "error": True, 
              "reason": "SQLi detected."
            }
  return None

def gather_resp_items(resp):
  to_check = []
  if 'json' in resp.headers['Content-Type']:
    to_check += flatten(resp.get_json())
  else:
    to_check += resp.get_data()
  return to_check

def gather_items(request, url):
  to_check = []
  if url is not None:
    to_check.append(url)
  
  for x in request.args:
    to_check.append(request.args.get(x))

  if request.method == 'POST':
    if 'json' in request.headers['Content-Type']:
      to_check += flatten(request.get_json())
  return to_check


def proxy(request__, url=None):
  new_url = f'http://{translate(request.host)}/'
  full_url = request.url.replace(request.host_url, new_url)

  to_check = gather_items(request, url)
  rules = get_rules_for_url(request.host)
  
  # Check request
  if rules is not None:
    bad = check_req(request.path, rules, to_check, 'in')
    if bad != None:
      return bad

  resp = requests.request(
    method=request.method,
    url=full_url,
    headers={key: value for (key, value) in request.headers if key != 'Host'},
    data=request.get_data(),
    cookies=request.cookies,
    allow_redirects=False
  )

  excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
  headers = [(name, value) for (name, value) in resp.raw.headers.items()
              if name.lower() not in excluded_headers]

  resp = Response(resp.content, resp.status_code, headers)

  if rules is not None:
    to_check = gather_resp_items(resp)
    bad = check_req(request.path, rules, to_check, 'out')
    if bad != None:
      return bad
  
  return resp