from app.main import app

PORT = 9000
HOST = '127.0.0.3'

app.run(host=HOST, port=PORT, debug=False, use_evalex=False)

