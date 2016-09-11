# -*- coding: utf-8 -*-

import boto3
import os
import json
from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

sns_client = boto3.client('sns', region_name='us-west-2')

@app.route('/result', methods=['POST'])
def process_result():
    req = request.get_json(force=True)
    game_id = req['gameID']
    sit_id = req['sitID']
    situation_result = retrieve_situation_result(game_id, sit_id)
    situation_player_choices = retrieve_player_choices(game_id, sit_id)
    scores = calculate_scores(situation_result, situation_player_choices)
    put_results(sns_client, scores)
    return '', 200


def retrieve_situation_result(game_id, sit_id):
    client = MongoClient("mongodb://{}:{}@ds029476.mlab.com:29476/team-awesome".format(os.getenv("MONGO_USER"),
                                                                                       os.getenv("MONGO_PASSWORD")))
    db = client['team-awesome']
    cursor = db.situation_results.find({"sitID": sit_id, "gameID": game_id})
    client.close()
    return cursor[0]


def retrieve_player_choices(game_id, sit_id):
    client = MongoClient("mongodb://{}:{}@ds029476.mlab.com:29476/team-awesome".format(os.getenv("MONGO_USER"),
                                                                                       os.getenv("MONGO_PASSWORD")))
    db = client["team-awesome"]
    cursor = db.player_choices.find({"sitID": sit_id, "gameID": game_id})
    client.close()
    return cursor


def calculate_scores(situation_result, situation_player_choices):
    score_json = {"gameID": situation_result["gameID"], "situationID": situation_result["sitID"], "playerScores": []}
    for player_choice in situation_player_choices:
        player_json = {"playerID": player_choice["playerID"]}
        player_score = 0
        if player_choice["choice"]["action"] == situation_result["result"]["action"]:
            player_score += 1
        if player_choice["choice"]["distance"] == situation_result["result"]["distance"]:
            player_score += 1
        if player_choice["choice"]["position"] == situation_result["result"]["position"]:
            player_score += 1
        player_json["score"] = player_score
        score_json["playerScores"].append(player_json)
    print score_json
    return score_json


def put_results(client, data):
    response = client.publish(
        TopicArn='arn:aws:sns:us-west-2:785203616251:gamestream-dev-scoreupdates',
        Message=json.dumps(data),
        MessageStructure='string',
    )

if __name__ == '__main__':
    app.run('0.0.0.0', os.getenv("ENGINE_PORT", "5000"))
