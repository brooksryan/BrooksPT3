import os
from flask import Flask, request
import brooksChat
import openai
import prompts

openai.api_key = os.environ.get('OPENAPI_KEY')

app = Flask(__name__)

@app.route('/', methods=['POST'])
def standard_response():
    
    print('\n'+'Question' + request.json['input_text'])
    
    input_text = request.json['input_text']
    
    prompt = prompts.simplified_prompt(input_text)

    output_text = brooksChat.doCompletion(input_text, prompt)

    print('\n'+'Answer:' + output_text)

    return {'output_text': output_text}

if __name__ == '__main__':
    app.run()

    # print "word" new line "word"