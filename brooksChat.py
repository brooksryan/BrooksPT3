import openai
import os
import prompts
openai.api_key = os.environ.get('OPENAPI_KEY')

PINECONE_KEY = os.environ.get('PINECONE_KEY')

import pinecone
pinecone.init(
    api_key=PINECONE_KEY,
    environment="us-east1-gcp"  # find next to API key
)
index_name = 'brooks-only-chat-messages'

embed_model = "text-embedding-ada-002"


index = pinecone.Index(index_name) # connect to index


def complete(prompt): # complete a prompt with a given model
    
    print(prompt)

    res = openai.Completion.create( # complete prompt
        model='davinci:ft-personal:brodie-small-2023-03-07-19-19-54',
        prompt=prompt,
        temperature=0.1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["###", "\\n###\\n","\n"]
        )
    return res['choices'][0]['text'].strip() # return the completion


limit = 5000
def retrieve(query, prompt):
    
    query = query

    current_prompt = prompt
    
    res = openai.Embedding.create( # embed query
        input=[query],
        engine=embed_model
    )

    xq = res['data'][0]['embedding'] # retrieve from Pinecone
    res = index.query(xq, top_k=2, include_metadata=True) # get relevant contexts
    contexts = [
        x['metadata']['chat'] for x in res['matches'] # extract the contexts
    ]
    # build our prompt with the retrieved contexts included
    prompt_start = current_prompt.prompt_start()
    # add query to prompt
    prompt_end = current_prompt.prompt_end()

    # append contexts until hitting limit
    for i in range(len(contexts)):
        if len("\n---\n".join(contexts[:i])) >= limit:
            prompt = (
                prompt_start +
                "\n---\n".join(contexts[:i-1]) +
                prompt_end
            )
            break
        elif i == len(contexts)-1:
            prompt = (
                prompt_start +
                "\n---\n".join(contexts) +
                prompt_end
            )
    return prompt


def doCompletion (query, prompt):
    created_prompt = retrieve(query, prompt)
    return complete(created_prompt)

