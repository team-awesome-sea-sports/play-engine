aws sqs send-message --message-body "{\"situationID\":\"abcdefg-7\",\"gameID\":\"xxxx-yyyy-zzzz\",\"playerID\":\"1111\",\"choice\":{\"action\":\"pass\",\"position\":\"right\",\"distance\":\"short\"}}" --queue-url https://sqs.us-west-2.amazonaws.com/785203616251/player-choices --profile sportshack
aws sqs send-message --message-body "{\"situationID\":\"abcdefg-7\",\"gameID\":\"xxxx-yyyy-zzzz\",\"playerID\":\"1112\",\"choice\":{\"action\":\"pass\",\"position\":\"left\",\"distance\":\"short\"}}" --queue-url https://sqs.us-west-2.amazonaws.com/785203616251/player-choices --profile sportshack
aws sqs send-message --message-body "{\"situationID\":\"abcdefg-7\",\"gameID\":\"xxxx-yyyy-zzzz\",\"playerID\":\"1113\",\"choice\":{\"action\":\"run\",\"position\":\"left\",\"distance\":\"long\"}}" --queue-url https://sqs.us-west-2.amazonaws.com/785203616251/player-choices --profile sportshack

aws sqs send-message --queue-url https://sqs.us-west-2.amazonaws.com/785203616251/situation-results --profile sportshack --message-body """{\"situationID\":\"abcdefg-7\",
              \"gameID\":\"xxxx-yyyy-zzzz\",
              \"clock\": \"14:20\",
              \"details\": \"/2016/PRE/2/MIN/SEA/plays/ea6b8dc6-795c-427e-b157-db2b730d9e69.json\",
              \"direction\": \"Left\",
              \"distance\": \"Short\",
              \"down\": 2,
              \"formation\": \"Shotgun\",
              \"id\": \"ea6b8dc6-795c-427e-b157-db2b730d9e69\",
              \"participants\": [
                {
                  \"id\": \"52b14c80-ffc5-4fd6-9a32-d07b261f0841\",
                  \"jersey\": 13,
                  \"name\": \"Shaun Hill\",
                  \"position\": \"QB\",
                  \"team\": \"MIN\"
                },
                {
                  \"id\": \"f77479d7-51a5-41f9-8924-69526dd078cd\",
                  \"jersey\": 21,
                  \"name\": \"Jerick McKinnon\",
                  \"position\": \"RB\",
                  \"team\": \"MIN\"
                }
              ],
              \"play_type\": \"pass\",
              \"sequence\": 4,
              \"side\": \"MIN\",
              \"summary\": \"13-S.Hill incomplete. Intended for 21-J.McKinnon.\",
              \"type\": \"play\",
              \"updated\": \"2016-08-19T02:10:58+00:00\",
              \"yard_line\": 24,
              \"yfd\": 8
            }"""
