import os
from flask import Flask, request
import brooksChat

app = Flask(__name__)

@app.route('/', methods=['POST'])
def add_period():
    print(request.json['input_text'])
    input_text = request.json['input_text']
    output_text = brooksChat.complete(brooksChat.retrieve(input_text))
    return {'output_text': output_text}

if __name__ == '__main__':
    app.run()