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

def complete(prompt, question): # complete a prompt with a given model
    
    print(f'\n Answering the question based on this prompt:{prompt}')

    print(f'\n question to be answered:{question}')

    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": f"{prompt}"},
                {"role": "user", "content": f"{question}"},
        ]
    )
    return res['choices'][0]['message']['content'].strip() # return the completion

class create_completion_prompt_v2:

    def __init__(self, query, prompt):
        self.query = query
        self.prompt = prompt

    def retrieve_question_embedding_v2(self):
        
        #take the question and get similar contexts

        res = openai.Embedding.create( # embed query
            input=[self.query],
            engine=embed_model
        )
        self.question_embedding = res['data'][0]['embedding'] # retrieve from Pinecone
        return self.question_embedding
        
    def retrieve_contexts_v2(self):
        res = index.query(self.question_embedding, top_k=2, include_metadata=True) # get relevant contexts
             
        self.contexts = [
            x['metadata']['chat'] for x in res['matches'] # extract the contexts
        ]
        print(res['matches'])
        
        return self.contexts
        
    def build_prompt_v2(self):
        
        limit = 1000
        # build our prompt with the retrieved contexts included
        prompt_start = self.prompt.assistant_prompt_start()
        # add query to prompt

        # append contexts until hitting limit
        for i in range(len(self.contexts)):
            if len("\n\n---\n\n".join(self.contexts[:i])) >= limit:
                prompt = (
                    prompt_start +
                    "\n\n---\n\n".join(self.contexts[:i-1])
                )
                break
            elif i == len(self.contexts)-1:
                prompt = (
                    prompt_start +
                    "\n\n---\n\n".join(self.contexts)
                )
        self.completed_prompt = prompt
        return self.completed_prompt
    
    def build_question_v2(self):
        self.completed_question = self.prompt.assistant_question_start() + self.query
        return self.completed_question