import uuid
from tqdm import tqdm
import json

with open('chatTranscripts\popCulture.json', encoding="utf8") as j:
  data = json.load(j)

dataList = []

for message in data['messages']:

    #if message type is not 'default' then skip it
    if message['type'] != 'Default':
       continue

    if message['content'] == '':
       continue

    author = ''

    content = message.get('content', '')

    #if message has embeds, then add embeds.title and embeds.description to content
    if message['embeds'] != []:
       content = content + message['embeds'][0].get('title', '') + message['embeds'][0].get('description', '')

    if message['author']['name'] == 'Brooms':
       author = 'Brooks'
    
    elif message['author']['name'] == 'mileseldon':
       author = 'Miles Eldon'
    
    elif message['author']['name'] == 'moon doggie':
       author = 'John Oberbeck'

    content = {
        'id': str(uuid.uuid4()),
        'chat': author + ': ' + content,
        'minDate': message['timestamp']  
  }
    #text = message.get('text', '')  # Use get() method to handle missing key
    #created_date = 
    #new_message = {'name': name, 'text': text, 'created_date': created_date}
    dataList.append(content)

from tqdm import tqdm

# Combine 10 consecutive items from "data" list, overlapping each other by 5 items
step = 5
window_size = 20
n = len(dataList)
cleaned_dataList = [dataList[i:i+window_size] for i in tqdm(range(0, n, step)) if i+window_size<=n]

merged_data = []
for item in tqdm(cleaned_dataList):
  newItem = {
  "minDate": item[0]['minDate'],
  "chat" : 'excerpt start: ' + item[0]['minDate'] + ' excerpt: ' + ' '.join([n['chat'] for n in item])
  }
  merged_data.append(newItem)

with open("cleansedPopCulture.json", "w") as f:
    json.dump(merged_data, f)

print(merged_data)