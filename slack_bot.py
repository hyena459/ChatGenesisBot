import logging
import os
import openai
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

openai.api_key = os.environ["OPENAI_API_KEY"]
app = App(token=os.environ["SLACK_BOT_TOKEN"])
logging.basicConfig(level=logging.DEBUG)

# @app.event("app_mention")
# async def command_handler(body, say):
#     logging.debug("Received app_mention event")
#     text = body['event']['text']
#     user = body['event']['user']
#     logging.debug(f"Received a message: {text}")

#     # メンションを取り除く
#     prompt = text.replace(f'<@{user}>', '').strip()

#     # GPT-3.5-turboを使ってリクエストを生成
#     response = openai.Completion.create(
#         engine="chatgpt-3.5-turbo",
#         prompt=prompt,
#         max_tokens=150,
#         n=1,
#         stop=None,
#         temperature=0.5,
#     )
#     # 返信を取得し、Slackに送信
#     reply = response.choices[0].text.strip()
#     logging.debug(f"Replyed a message: {reply}")
#     await say(f'<@{user}> {reply}')

@app.event("app_mention")
async def test_handler(body, say):
    print("Test handler triggered")
    try:
        await say("Hello, I'm here!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()