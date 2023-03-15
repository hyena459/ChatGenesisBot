import os
import openai
import re
import json
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

app = Flask(__name__)

openai.api_key = os.environ["OPENAI_API_KEY"]
slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

def chatgpt_query(prompt):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].text.strip()
    return message

@app.route('/slack/events', methods=['POST'])
def handle_slack_event():
    payload = request.form.get("payload")
    if payload:
        payload = json.loads(payload)
        if "challenge" in payload:
            return payload["challenge"]

    event = json.loads(request.form["payload"])["event"]

    if event.get("type") == "app_mention":
        text = event['text']
        bot_user_id = event['user']
        channel = event['channel']

        prompt = re.sub(f"<@{bot_user_id}>", "", text).strip()

        try:
            response = chatgpt_query(prompt)
            slack_client.chat_postMessage(channel=channel, text=response)
        except openai.OpenAIError as e:
            print(f"OpenAI Error: {e}")
            slack_client.chat_postMessage(channel=channel, text="エラーが発生しました。しばらくしてからもう一度お試しください。")
        except SlackApiError as e:
            print(f"Slack API Error: {e}")

    return ('', 204)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
