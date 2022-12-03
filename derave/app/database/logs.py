import sqlite3

def serialize(x):
  try:
    return {
      "id": x[0],
      "type": x[1],
      "src": x[2],
      "res": x[3],
      "user_agent": x[4],
      "timestamp": x[5]
    }
  except:
    return None

def add_log(reqtype, src, res, agent):
  conn = sqlite3.connect('app/database/database.db')
  
  query = 'insert into logs(type,src_ip,resource,user_agent) values(?,?,?,?)'

  cur = conn.cursor()
  cur.execute(query, (reqtype, src, res, agent))
  conn.commit()
  conn.close()

def view_logs():
  conn = sqlite3.connect('app/database/database.db')
  
  query = 'select * from logs limit 50'
  cur = conn.cursor()
  res = cur.execute(query)
  logs = res.fetchall()

  return [serialize(x) for x in logs]