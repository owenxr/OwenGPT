import message_reader
import message_sender
import texter_model
import csv
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Create an empty list to hold the dictionaries
contacts = {}

# Open the CSV file and read the data
with open('contacts.csv', mode='r') as file:
    # Create a CSV reader
    csv_reader = csv.DictReader(file)

    # Process each row in the file
    for row in csv_reader:
        key = row['number']
        contacts[key] = row['name']

# print(contacts)

for c in test_contacts:
    pretext = message_reader.read_texts(c)
    print(pretext)
    responses = texter_model.gen_responses(pretext)
#    print(responses)
    for response in responses:
        if test_contacts[c] == 'SMS':
            message_sender.send_sms(c, response)
        else:
            message_sender.send_imessage(c, response)
