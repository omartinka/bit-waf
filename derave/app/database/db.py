import sqlite3

def init_db():
  conn = sqlite3.connect('app/database/database.db')
  with open('app/database/schema.sql', 'r') as f:
    conn.executescript(f.read())

  try:
    conn.execute("insert into users(name, password, privileges) values (?, ?, 1)", ('admin', 'futbal123'))
    conn.commit()
  except:
    pass
  
  conn.close()