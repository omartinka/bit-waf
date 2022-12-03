from app.main import app
from app.database.db import init_db

PORT = 9000
HOST = '127.0.0.2'

init_db()

app.run(host=HOST, port=PORT, debug=True, use_evalex=False)

