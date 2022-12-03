import pandas as pd
import csv
from urllib.parse import unquote
from model.parser import Parser

class ParserXSS(Parser):
  def __init__(self):
    pass

  def parse_line(self, line):
    parsed = {}
    orig = line
    try:
      line = unquote(line)
    except:
      pass
    nospaces = line.replace('\n', '')
    nospaces = nospaces.replace('\t', '')
    nospaces = nospaces.replace(' ', '').lower()
    parsed['tags'] = 0
    for x in ['div', 'svg', 'image', 'image', 'script', 'style', 'element', 'audio']:
        if x in nospaces:
            parsed['tags'] = 1
    
    parsed['functions'] = 0
    for x in ['eval', 'alert', 'log']:
        if x in nospaces:
            parsed['functions'] = 1
    
    parsed['objects'] = 0
    for x in ['document', 'window', 'iframe', 'location', 'console']:
        if x in nospaces:
            parsed['objects'] = 1
    
    parsed['events'] = 0
    for x in [' onerror', ' onload']:
        if x in line:
            parsed['events'] = 1
    
    parsed['length'] = len(line)
    parsed['alphanum'] = self.count_an(line)
    parsed['special'] = self.count_special(line)
    
    one_chars = ['(', ')', '<', '>', '/', '_', '.']
    for c in one_chars:
        parsed[c] = self.count_char(line, c)
    
    return pd.Series([
        parsed['tags'], 
        parsed['functions'], 
        parsed['objects'], 
        parsed['events'], 
        parsed['length'], 
        parsed['alphanum'], 
        parsed['special'],
        parsed['('],
        parsed[')'],
        parsed['<'],
        parsed['>'],
        parsed['/'],
        parsed['_'],
        parsed['.'],
        ');' in line,
        '</' in line,
        '//' in line,
        '&lt' in orig,
        '&gt' in orig
    ])

parser_xss = ParserXSS()