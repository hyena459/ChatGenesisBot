import os
import openai
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from time import sleep

openai.api_key = os.environ["OPENAI_API_KEY"]
app = App()

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

@app.event("app_mention")
async def command_handler(body, say):
    text = body['event']['text']
    bot_user_id = body['event']['user']

    # ボットのユーザー名部分を削除
    prompt = re.sub(f"<@{bot_user_id}>", "", text).strip()

    try:
        response = chatgpt_query(prompt)
        await say(response)
    except openai.OpenAIError as e:
        print(f"OpenAI Error: {e}")
        await say("エラーが発生しました。しばらくしてからもう一度お試しください。")
    except Exception as e:
        print(f"Error: {e}")
        await say("予期しないエラーが発生しました。")
    finally:
        sleep(1)  # レート制限のためのスリープ

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()