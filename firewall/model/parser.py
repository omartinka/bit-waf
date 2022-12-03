import pandas as pd
import csv
from urllib.parse import unquote

class Parser:
  def __init__(self):
    pass
  
  def parse_all(self, data):
    toret = {}
    for line in data.rows:
        obj = self.parse_line(line)
        for x in obj:
            if x not in toret:
                toret[x] = []
            toret[x].append(obj[x])
    return toret
  
  def contains(self, data, char):
    return char in data

  def count_char(self, string, char):
    count = 0
    for x in string:
        if x == char:
            count += 1
    return count & 1
  
  def count_an(self, string):
    count = 0
    for x in string:
        if (ord(x) >= 48 and ord(x) <= 57) or (ord(x) >= 65 and ord(x) <= 90) or (ord(x) >= 97 and ord(x) <= 122):
            count += 1
    return count

  def contains_regex(self, string):
    pass

  def count_special(self, line):
    return len(line) - self.count_an(line)
  
  # virtual func
  def parse_all(self, data):
    return {}