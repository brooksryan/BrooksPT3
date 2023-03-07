import os
from flask import Flask, request
import brooksChat
import brooksChat002
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

# for /v2 route method post - uses turbo gpt-3.5 but results honestly arent that great
@app.route('/v2', methods=['POST'])
def standard_response_v2():
    
    print('\n'+'Raw Question: ' + request.json['input_text'])
    
    input_text = request.json['input_text']

    selected_prompt_formatter = prompts.standard_prompt_v2(input_text)

    #feed the prompt and the question to the new v2 completion function
    print(selected_prompt_formatter.assistant_prompt_start())

    prompt_and_context_tool = brooksChat002.create_completion_prompt_v2(input_text, selected_prompt_formatter)
    prompt_and_context_tool.retrieve_question_embedding_v2()
    prompt_and_context_tool.retrieve_contexts_v2()
    prompt_and_context_tool.build_prompt_v2()
    prompt_and_context_tool.build_question_v2()

    output_text = brooksChat002.complete(prompt_and_context_tool.completed_prompt, prompt_and_context_tool.completed_question)

    print('\n'+'Answer:' + output_text)
    return {'output_text': output_text}

if __name__ == '__main__':
    app.run()

    # print "word" new line "word"