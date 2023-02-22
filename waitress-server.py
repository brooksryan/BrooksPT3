from waitress import serve
import app
import os

OPENAPI_KEY = os.environ.get('OPENAPI_KEY')
serve(app.app, host='127.0.0.1', port=5000)