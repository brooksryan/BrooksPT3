import openai
import os
import pandas as pd
from tqdm import tqdm

tqdm.pandas()

openai.api_key = os.environ.get('OPENAPI_KEY')
PINECONE_KEY = os.environ.get('PINECONE_KEY')

# open th efinle cleansedChockStoneworks.json using pandas
# initialJsonLoad = pd.read_json("chatTranscripts\cleansedChockStoneworks.json")

# df=initialJsonLoad.head(100)


# create function to get questions from openai
def get_questions(context):
    try:
        response = openai.Completion.create(
            engine="text-curie-001",
            prompt=f"Write questions About Brooks's life based on the text below\n\nText: {context}\n\nQuestions:\n1.",
            temperature=0,
            max_tokens=257,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n\n"]
        )
        print
        return response['choices'][0]['text']
    except Exception as e:
        print(e)
        quit()


# create json file with questions from df
def createJsonWithQuestions(json, outputFileName):
    df = pd.read_json(json)
    # apply get_questions to df['chat'] and save to df['questions'] and track progress with tqdm
    df['questions'] = df['chat'].progress_apply(get_questions)
    df['questions'] = "1." + df.questions

    # save df to new json file withQuestionsCleansedChockStoneworks.json
    df.to_json(outputFileName) 


# create function to get answers from openai
def get_answers(row):
    try:
        response = openai.Completion.create(
            engine="davinci-instruct-beta-v3",
            prompt=f"Write a fact about brooks based on the context below\n\nText: {row.chat}\n\nQuestions:\n{row.questions}\n\nAnswers:\n1.",
            temperature=0,
            max_tokens=257,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response['choices'][0]['text']
    except Exception as e:
        print (e)
        return ""
    
# apply get_answers to df['chat'] and save to df['answers'] and track progress with tqdm
def createJsonWithAnswers(json, outputFileName):
    df = pd.read_json(json)
    df['answers']= df.progress_apply(get_answers, axis=1) 
    df['answers'] = "1." + df.answers
    df = df.dropna().reset_index().drop('index',axis=1)

    # save df to new json file withQuestionsCleansedChockStoneworks.json
    df.to_json(outputFileName)


# turn json file into csv file
def loadJsonDfToCsv(jsonFile, outputPath):
    df = pd.read_json(jsonFile)
    df.to_csv(outputPath, index=False)


# load csv file, create new list of dictionaries, for each row in csv file create a dictionary with prompt, answer where prompt concatenates a prompt string, chat, and question and answer is equal to answer
def createJsonForPinecone(csvFile, outputPath):
    df = pd.read_csv(csvFile)

    newPrompt = "You are Brooks's personal assistant named BRODIE which stands for Brooks' Response Output on Discord with Intelligent Embeddedness. Answer only questions about Brooks using the context below. If the input is not a question, say you can only answer questions about Brooks:\n"

    data = []
    for index, row in df.iterrows():
        for q, a in zip(("1." + row.questions).split('\n'), ("1." + row.answers).split('\n')): #
            data.append({
                "prompt":f" {row.chat}\nQuestion: {q[2:].strip()}\nAnswer:\n", "completion":f" {a[2:].strip()}\n\n###\n\n"
            })
    df = pd.DataFrame(data)
    df.to_json(outputPath, orient='records', lines=True)

createJsonForPinecone("chatTranscripts\completionTrainingData\CompletionForChockStoneworks.csv", "chatTranscripts\completionTrainingData\ConcatenatedTrainingCompletionForChockStoneworks.json")

# context = "excerpt start: 2021-03-08T19:17:17.71+00:00 excerpt: John Oberbeck: howdoyouturnthison Brooks: lol Brooks: moondoggie John Oberbeck: i was leaning in to discor John Oberbeck: *discord John Oberbeck: okay John Oberbeck: care and feeding of discord John Oberbeck: what are the best tricks to know John Oberbeck: \u00af\\_(\u30c4)_/\u00af John Oberbeck: https://tenor.com/bqLQZ.gif John Oberbeck: SO much less time searching for gifs Brooks: oh yeah Brooks: spotify links work and open to the app Brooks: at least for me John Oberbeck: how did you get to brooms? Brooks: Like how did I settle on that as a name? John Oberbeck: ya Brooks: Brooks -> Books -> Wooks -> Brooms Brooks: is how the progression went with SCU people John Oberbeck: well alright then"

# if __name__ == "__main__":
    
#     chatJson = sys.argv[1] # this is the data that is passed in from the waitress server

#     df = pd.read_json("cleansedChockStoneworks.json", lines=True) 

