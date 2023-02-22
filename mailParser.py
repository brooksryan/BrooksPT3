import mailbox
import re
from tqdm import tqdm
import json
import uuid

mbox = mailbox.mbox('C:/Users/brook/OneDrive/0.active/googleTakeout/mailTakeout/Mail/Sent.mbox')

# mailboxLength = len(mbox)
emailList = []

#keys = mbox.keys()

#print(keys)

def clean_text(text):
    
    #create empty string for appending text:
    bodyString = ''

    for i in text :
        cleanedLine = str(i)
        # print(type(cleanedLine))
        longword = re.compile(r'\W*\b\w{16,}\b')
        cleanedLine = re.sub(longword, '', cleanedLine) #remove long words
        cleanedLine = cleanedLine.replace("\n", "")  #remove new lines
        cleanedLine = cleanedLine.replace(">", "")  #remove new lines
        
        cleanedLine = re.sub('<[^<]+?>', '', cleanedLine) #remove html tags
        #cleanedLine = re.sub(r'\[.*?\]', '', cleanedLine)
        bodyString = bodyString + cleanedLine #append cleaned line to bodyString

    # print(type(bodyString))
    return str(bodyString) #return the cleaned body


for i in tqdm(range(len(mbox))):

# for i in tqdm(range(49,50)):

    #print(mbox.get_string(i))

    # get the sender of the email
    sender = str(mbox[i]['from'])
    
    # get the body of the email
    # body= mbox.get_string(i)
    body= [part.get_payload() for part in mbox[i].walk() if part.get_content_type() == 'text/plain']
    # print(body)

    # print the type of the body variable
    # print(len(body))
       
    cleanedBody = clean_text(body)

    
    
    # if the sender is not Brooks or the body is empty, skip the email
    if cleanedBody == '' :
        continue

    # get the date of the email
    date = str(mbox[i]['date'])

    # get the subject of the email
    subject = str(mbox[i]['subject'])
   
    text = 'On ' + date[:16] + " " + sender + "wrote: " + cleanedBody[:10000]

    emailContent = {
        
        #randomUUID
        'id': str(uuid.uuid4()),

        #naming minDate becuase that's what I called it in the gchat parser
        'minDate': date,

        #naming chat because the that's what I called it in the gChat parser
        'chat': text,

    }

    emailList.append(emailContent)
    # print(emailContent)

# print(emailList)

# Write the Python object into the file
with open("brooksCleansedEmailsBetterRegexLonger.json", "w") as f:
    json.dump(emailList, f)