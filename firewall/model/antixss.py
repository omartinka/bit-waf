from model.parser_xss import parser_xss
import sys
import numpy as np
from sklearn import svm
from sklearn.metrics import classification_report
import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler 
from model.arghelper import check_arg

class AntiBase:
  def __init__(self):
    self.class_col = 'tmp'
    self.parser = None
    
  # Loads a dataset, parses it, trains the model and saves it as a local file
  # if told to
  def train(self, dataset):
    # Load the dataset
    self.df = pd.read_csv(dataset, sep='\t', engine='python', quoting=3)
    self.df = self.df.drop_duplicates()
    self.df['payload'] = self.df.payload.astype(str)
    self.df = self.df.sample(frac=1)

    self.df[self.cols] = self.df['payload'].apply(self.parser.parse_line)
    self.df = self.df.drop(['payload'], axis=1)

    # Process and scale
    self.scaler = MinMaxScaler()
    self.df[self.cols] = self.scaler.fit_transform(self.df[self.cols].to_numpy())

    # Split into train and test dataset
    df_test   = self.df[:int(len(self.df)/2.5)]
    df_train  = self.df[int(len(self.df)/2.5):]

    # Train the model
    X_train, y_train = df_train.loc[:, df_train.columns != self.class_col], df_train.loc[:, self.class_col]
    X_test, y_test = df_test.loc[:, df_test.columns != self.class_col], df_test.loc[:, self.class_col]

    self.clf = svm.SVC()
    self.clf = self.clf.fit(X_train.to_numpy(), y_train.to_numpy())
    y_pred = self.clf.predict(X_test.to_numpy())
    print('[!] Training done!')
    print(classification_report(y_test, y_pred))

    self.trained = True
    joblib.dump(self.scaler, f'./data/scaler_{self.class_col}.bin')
    joblib.dump(self.clf, f'./data/{self.class_col}.bin')

# Helper class yadayadayoo
class AntiXSS(AntiBase):
  def __init__(self):
    self.class_col = 'xss'
    self.trained = False
    self.parser = parser_xss
    self.cols = ['tags','functions', 'objects', 'events', 'length', 'alphanum', 'special','(',')','<','>','/','_','.', ');', '</', '//', '&lt', '&gt']
    if '--xss' in sys.argv:
      filename = sys.argv[sys.argv.index('--xss')+1]
      self.load(filename)
      print(f'[+] Loaded model {filename}')

    elif '--train-xss' in sys.argv:
      dataset_file = sys.argv[sys.argv.index('--train-xss')+1]
      dataset = f'./data/{dataset_file}'
      self.train(dataset) 
 
  # Loads model from a file
  def load(self, file):
    self.scaler = joblib.load(f'./data/scaler_{file}')
    self.clf = joblib.load(f'./data/{file}')
    self.trained = True

  # Check whether the input looks sus
  # returns:
  #  - True if inputs looks OK
  #  - False if malicious  
  def check(self, arr):
    if self.trained == False:
      print('[!] Model not trained')
      return True

    if len(arr) == 1:
      print('[!!!] CEHCKING:', arr[0])
      res1 = parser_xss.parse_line(arr[0])
      res2 = self.scaler.transform(res1.to_numpy().reshape(1, -1))
      res3 = self.clf.predict(res2)
      if res3[0] == 1:
        return False
    else:
      for x in arr:
        print('[!!!] CEHCKING:', x)
        res1 = parser_xss.parse_line(x)
        res2 = self.scaler.transform(res1.to_numpy().reshape(1, -1))
        res3 = self.clf.predict(res2)
        if res3[0] == 1:
          return False
      return True

anti_xss = AntiXSS()