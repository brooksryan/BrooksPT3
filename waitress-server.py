from waitress import serve
import app
import os

OPENAPI_KEY = os.environ.get('OPENAPI_KEY')
serve(app.app, host='localhost', port=5000)