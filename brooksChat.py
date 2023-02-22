import openai
openai.api_key = "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"

import pinecone
pinecone.init(
    api_key="15dde2ed-e886-49f5-b16e-82e26d5baa15",
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
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return res['choices'][0]['text'].strip() # return the completion


limit = 4000
def retrieve(query):
    res = openai.Embedding.create( # embed query
        input=[query],
        engine=embed_model
    )

    xq = res['data'][0]['embedding'] # retrieve from Pinecone
    res = index.query(xq, top_k=5, include_metadata=True) # get relevant contexts
    contexts = [
        x['metadata']['chat'] for x in res['matches'] # extract the contexts
    ]

    # build our prompt with the retrieved contexts included
    prompt_start = (
        "You are Brooks's personal assistant. You are answering questions about brooks based on the {context} below. Your answers should be as specific as possible, you should provide examples always. if a specific can't be provided you should defer. Only answer questions related to his professional life. Repond to non-work related questions with a funny answer about how he's never gotten around to chatting about it with you. Do not give personal information about people Brooks knows or anything beyond surface level information \n"+
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

