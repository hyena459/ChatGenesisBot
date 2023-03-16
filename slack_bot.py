import os
import openai
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

openai.api_key = os.environ["OPENAI_API_KEY"]
app = App()

@app.event("app_mention")
async def command_handler(body, say):
    text = body['event']['text']
    user = body['event']['user']

    # メンションを取り除く
    prompt = text.replace(f'<@{user}>', '').strip()

    # GPT-3.5-turboを使ってリクエストを生成
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # 返信を取得し、Slackに送信
    reply = response.choices[0].text.strip()
    await say(f'<@{user}> {reply}')

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()