# -*- coding: utf-8 -*-

"""
[module name here]
~~~~~~~~~~~~~~~~~

[Description here]

"""
import boto3
import os
import json
from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

sns_client = boto3.client('sns', region_name='us-west-2')

json_publish = {
  "gameID": "1234",
  "situationID": "1234",
  "playerScores": [
    {
      "playerID": "1234",
      "score": "29"
    },
    {
      "playerID": "5678",
      "score": "56"
    }
  ]
}


@app.route('/result', methods=['POST'])
def process_result():
    req = request.get_json(force=True)
    game_id = req['gameID']
    sit_id = req['sitID']
    print game_id, sit_id
    # situation_result = retrieve_situation_result(game_id, sit_id)
    # situation_player_choices = retrieve_player_choices(game_id, sit_id)
    # scores = calculate_scores(situation_result, situation_player_choices)
    # put_results(sns_client, scores)
    return '', 201


def retrieve_situation_result(game_id, sit_id):
    client = MongoClient("mongodb://{}:{}@ds029476.mlab.com:29476/team-awesome".format(os.getenv("MONGO_USER"),
                                                                                       os.getenv("MONGO_PASSWORD")))
    db = client["team-awesome"]
    cursor = db.situation_results.find({"sitID": sit_id, "gameID": game_id})
    client.close()
    return cursor


def retrieve_player_choices(game_id, sit_id):
    client = MongoClient("mongodb://{}:{}@ds029476.mlab.com:29476/team-awesome".format(os.getenv("MONGO_USER"),
                                                                                       os.getenv("MONGO_PASSWORD")))
    db = client["team-awesome"]
    cursor = db.player_choices.find({"sitID": sit_id, "gameID": game_id})
    client.close()
    return cursor


def calculate_scores():
    pass


def put_results(client, data):
    response = client.publish(
        TopicArn='arn:aws:sns:us-west-2:785203616251:gamestream-dev-scoreupdates',
        Message=json.dumps(data),
        MessageStructure='string',
    )
    print response

if __name__ == '__main__':
    app.run('0.0.0.0', '5000')
