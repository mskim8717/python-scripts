import requests
import json


def post_message(channel, text):
    SLACK_BOT_TOKEN = "TOKEN_VALUE"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + SLACK_BOT_TOKEN
        }
    payload = {
        'channel': channel,
        'text': text
        }
    r = requests.post('https://slack.com/api/chat.postMessage',
        headers=headers,
        data=json.dumps(payload)
        )


if __name__ == '__main__':
    post_message("#autobot", "Hello World!")