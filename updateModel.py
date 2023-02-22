from tqdm.auto import tqdm
import os
import datetime
from time import sleep
import uuid

# Import open AI
import openai
openai.api_key = os.environ.get('OPENAPI_KEY')

# initialize connection (get API key at app.pinecone.io)
import pinecone
pinecone.init(
    api_key="15dde2ed-e886-49f5-b16e-82e26d5baa15",
    environment="us-east1-gcp"  # find next to API key
)

index_name = 'brooks-only-chat-messages'
embed_model = "text-embedding-ada-002"

#get dimensions from sample embedding
def get_length_of_embedding(embed_model):
    res = openai.Embedding.create( 
        input=[
            "Sample document text goes here"
        ], engine=embed_model
    )
    return len(res['data'][0]['embedding']) # check number of dimensions

# Connect to pinecone instance, create index if it does not exist
def create_index(index_name, embeddings):
    if index_name not in pinecone.list_indexes(): # if does not exist, create index
    
        pinecone.create_index( # create index
            index_name, 
            dimension= embeddings, # dimension of embeddings
            metric='cosine',
            metadata_config={
                'indexed': ['chat']
            }
        )
    index = pinecone.Index(index_name) # connect to index
    index.describe_index_stats() # view index stats


from tqdm.auto import tqdm
import datetime
from time import sleep
import uuid

batch_size = 100  # how many embeddings we create and insert at once

def upsert_to_pinecone(merged_data, index):
    # iterate over batches of data
    for i in tqdm(range(0, len(merged_data), batch_size)):
        # find end of batch
        i_end = min(len(merged_data), i+batch_size)
        meta_batch = merged_data[i:i_end]
        # get ids
        ids_batch = [str(uuid.uuid4()) for x in meta_batch]
        # get texts to encode
        texts = [x['chat'] for x in meta_batch]
        # create embeddings (try-except added to avoid RateLimitError)
        try:
            res = openai.Embedding.create(input=texts, engine=embed_model)
        except:
            done = False
            while not done:
                sleep(5)
                try:
                    res = openai.Embedding.create(input=texts, engine=embed_model)
                    done = True
                except:
                    pass

        # now the embeds retrieved from the openai response in res['data'] 
        embeds = [record['embedding'] for record in res['data']]
        
        # cleanup metadata
        meta_batch = [{
            'chat': x['chat'],
            'minDate': x['minDate'],
        } for x in meta_batch]

        #creates the ids, embeds and metabatch to upsert to pinecone
        to_upsert = list(zip(ids_batch, embeds, meta_batch))
        
        # upsert to Pinecone
        index.upsert(vectors=to_upsert)
