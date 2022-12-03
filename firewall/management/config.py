from collections import Iterable
from copy import deepcopy
import os
import json

def translate(url):
  try:
    global ruleset
    for elem in ruleset:
      if elem['host'] == url:
        return elem['ip']
  except:
    return None

def get_rules_for_url(url):
  try:
    global ruleset
    for elem in ruleset:
      if elem['host'] == url:
        return elem['ruleset']
  except:
    return None
  return None

def save_ruleset():
  global default_rules, ruleset
  with open(default_rules, 'w') as f:
    json.dump(ruleset, f)
    print(ruleset)

def init_ruleset():
  global default_rules, ruleset
  with open(default_rules, 'r') as f:
    ruleset = json.load(f)

def get_ruleset():
  return deepcopy(ruleset)

def set_ruleset(_ruleset):
  global ruleset
  ruleset = _ruleset
  save_ruleset()

# https://stackoverflow.com/questions/23619568/mapping-nested-dictionaries-in-python
def flatten(x):
  result = []
  if isinstance(x, dict):
    x = x.values()
  for el in x:
    if isinstance(el, Iterable) and not isinstance(el, str):
      result.extend(flatten(el))
    else:
      result.append(el)
  return result

ruleset = {}
default_rules = '.ruleset'
if os.environ['FILE_RULESET'] != None:
  default_rules = os.environ['FILE_RULESET']
init_ruleset()