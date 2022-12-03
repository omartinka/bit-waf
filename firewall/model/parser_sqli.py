import pandas as pd
import csv
from urllib.parse import unquote
from model.parser import Parser

class ParserSqli(Parser):
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
    parsed['control'] = 0
    for x in ['select', 'where', 'union']:
        if x in nospaces:
            parsed['control'] = 1
    
    parsed['functions'] = 0
    for x in ['exec', 'sleep']:
        if x in nospaces:
            parsed['functions'] = 1
        
    parsed['length'] = len(line)
    parsed['alphanum'] = self.count_an(line)
    parsed['special'] = self.count_special(line)
    
    return pd.Series([
        parsed['control'], 
        parsed['functions'], 
        parsed['length'], 
        parsed['alphanum'], 
        parsed['special'],
        '(' in line,
        ')' in line,
        '--' in line,
        '=' in line,
        '%' in line,
        '\'' in orig,
        '"' in orig
    ])

parser_sqli = ParserSqli()