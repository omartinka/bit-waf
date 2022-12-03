from model.parser_sqli import parser_sqli
from model.antixss import AntiBase
import sys
import numpy as np
from sklearn import svm
from sklearn.metrics import classification_report
import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler 
from model.arghelper import arg_pos, check_arg

DEBUG=True

class AntiSqli(AntiBase):
  def __init__(self):
    self.class_col = 'sqli'
    self.parser = parser_sqli
    self.trained = False
    self.cols = [
      'tags','functions', 'length', 'alphanum', 'special',
      '(', ')', '--', '=', '%', '\'' ,'"'
    ]

    pos_model = arg_pos('--sqli', '-s')
    pos_dataset = arg_pos('--train-sqli', '-ts')

    if pos_model is not None:
      filename = sys.argv[pos_model+1]
      self.load(filename)
      print('[+] Loaded model {filename}')

    elif pos_dataset is not None:
      dataset_file = sys.argv[pos_dataset+1]
      dataset = f'./data/{dataset_file}'
      print('training...')
      self.train(dataset)

  def load(self, file):
    self.scaler = joblib.load(f'./data/scaler_{file}')
    self.clf = joblib.load(f'./data/{file}')
    self.trained = True
  
  def check(self, arr):
    if self.trained == False:
      print('[!] Model not trained')
      return True

    for x in arr:
      if DEBUG:
        print('[!!!] Checking', x)
      res1 = self.parser.parse_line(x)
      res2 = self.scaler.transform(res1.to_numpy().reshape(1, -1))
      res3 = self.clf.predict(res2)
      if res3[0] == 1:
        return False
    return True

anti_sqli = AntiSqli()