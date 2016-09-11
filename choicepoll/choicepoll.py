import boto3
import json
import flask
import os

from pymongo import MongoClient

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

region_name = 'us-west-2'
queue_name = 'player-choices'
max_queue_messages = 10
message_bodies = []
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
sqs = boto3.resource('sqs', region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)
queue = sqs.get_queue_by_name(QueueName=queue_name)

# dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="https://dynamodb.us-west-2.amazonaws.com")
mongoClient = MongoClient("mongodb://{}:{}@ds029476.mlab.com:29476/team-awesome".format(os.getenv("MONGO_USER"), os.getenv("MONGO_PASSWORD")))

while True:
    messages_to_delete = []
    for message in queue.receive_messages(MaxNumberOfMessages=max_queue_messages):
        # process message body
        messageBody = str.lower(message.body)
        body = json.loads(messageBody)
        message_bodies.append(body)
        # add message to delete
        messages_to_delete.append({
            'Id': message.message_id,
            'ReceiptHandle': message.receipt_handle
        })

        print ('Log -> Received content: ', body)
        db = mongoClient['team-awesome']
        coll = db['player_choices']
        try:
            result = db.player_choices.insert_one (
                {"sitID":body['situationid'],
                 "gameID":body['gameid'],
                 "playerID":body['playerid'],
                 "choice":body['choice']
                 }
            )
            print ("mongo result: ", result.inserted_id)
        except:
            print ('There was an error posting to Mongo')
            
    # if you don't receive any notifications the
    # messages_to_delete list will be empty
    if len(messages_to_delete) == 0:
        continue
    # delete messages to remove them from SQS queue
    # handle any errors
    else:
        print('Deleting messages: ', messages_to_delete)
        delete_response = queue.delete_messages(
                Entries=messages_to_delete)
