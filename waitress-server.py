from waitress import serve
import app
import os

BROOKSPT3_HOST = os.environ.get('BROOKSPT3_HOST')
BROOKSPT3_PORT = os.environ.get('BROOKSPT3_PORT')
OPENAPI_KEY = os.environ.get('OPENAPI_KEY')
serve(app.app, host=BROOKSPT3_HOST, port=BROOKSPT3_PORT)