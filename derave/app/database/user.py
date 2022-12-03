import sqlite3

def serialize(user):
  try:
    return {
      "id": user[0],
      "name": user[1],
      "pass": user[2],
      "privileges": user[3]
    }
  except:
    return None

def register_user(username, password):
  conn = sqlite3.connect('app/database/database.db')

  query = "insert into users(name, password, privileges) values (?, ?, 0)"

  cur = conn.cursor()
  cur.execute(query, (username, password))
  conn.commit()
  conn.close()

  return login_user(username, password)

def login_user(username, password):
  conn = sqlite3.connect('app/database/database.db')
  query = f"select * from users where name = '{username}' and password = '{password}'"
  cur = conn.cursor()
  res = cur.execute(query)
  user = res.fetchone() 
  conn.close()
  return serialize(user)
