import openai
from Ayra import *

from .. import async_searcher, udB


async def get_chatbot_reply(message):
    chatbot_base = "https://kora-api.vercel.app/chatbot/2d94e37d-937f-4d28-9196-bd5552cac68b/{ayra_bot}/envparse/message={}"
    req_link = chatbot_base.format(
        message,
    )
    try:
        return (await async_searcher(req_link, re_json=True)).get("reply")
    except Exception:
        LOGS.info(f"**ERROR:**`{format_exc()}`")


class OpenAi:
    def text(self, question):
        OPENAI_API = udB.get_key("OPENAI_API")
        openai.api_key = OPENAI_API
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Q: {question}\nA:",
            temperature=0,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return response.choices[0].text

    def photo(self, question):
        OPENAI_API = udB.get_key("OPENAI_API")
        openai.api_key = OPENAI_API
        response = openai.Image.create(prompt=question, n=1, size="1024x1024")
        return response["data"][0]["url"]
