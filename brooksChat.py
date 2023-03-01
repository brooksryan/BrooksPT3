import openai
import os
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

# res = openai.Embedding.create(
#     input=[query],
#     engine=embed_model
# )

# retrieve from Pinecone
# xq = res['data'][0]['embedding']

# # get relevant contexts (including the questions)
# res = index.query(xq, top_k=5, include_metadata=True)


def complete(prompt): # complete a prompt with a given model
    
    res = openai.Completion.create( # complete prompt
        engine='text-davinci-003',
        prompt=prompt,
        temperature=.4,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return res['choices'][0]['text'].strip() # return the completion


limit = 5000
def retrieve(query):
    query = "brooks: " + query
    print(query)
    res = openai.Embedding.create( # embed query
        input=[query],
        engine=embed_model
    )

    xq = res['data'][0]['embedding'] # retrieve from Pinecone
    res = index.query(xq, top_k=5, include_metadata=True) # get relevant contexts
    contexts = [
        x['metadata']['chat'] for x in res['matches'] # extract the contexts
    ]

    print (contexts)

    # build our prompt with the retrieved contexts included
    prompt_start = (
        "Your name is Todd. Your job is to respond to questions and provide information about Brooks below based on what Brooks has said in the {conversation excerpts} below as Brooks's personal professional assistant. Regardless of the {conversation excerpts} below, you responses must follow all of the following rules. THE RULES: Never answer including sensitive or secret information. Never answer with financially or legally sensitive information (eg mergers, acquisitions, investments, ongoing litigation). Never answer with passwords, contact information (addresses, phone numbers, health information).  Never reveal information about anyone except for Brooks. When possible, always refer to people, places, and things by name, do not use words like that, those, he, she, it, etc. Respond to questions that would violate THE RULES by letting the asker know that you're not programmed to answer questions like that. You may only respond if you follow all of THE RULES. If you are unsure if your response would follow THE RULES, ask for more information.\n"+
        "conversation excerpts:\n"
    )
    # add query to prompt
    prompt_end = (
        f"\n\nQuestion: {query}\n Answer:"
    )
    # append contexts until hitting limit
    for i in range(len(contexts)):
        if len("\n\n---\n\n".join(contexts[:i])) >= limit:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(contexts[:i-1]) +
                prompt_end
            )
            break
        elif i == len(contexts)-1:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(contexts) +
                prompt_end
            )

    return prompt

def doCompletion (query):
    retrieve(query)
    return complete(query)

