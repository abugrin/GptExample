import logging
import os
from dotenv import load_dotenv
from yambot import MessengerBot
from yambot.types import Update
from yandex_cloud_ml_sdk import YCloudML
from langchain_core.messages import AIMessage, HumanMessage

load_dotenv()
yb = MessengerBot(os.getenv('BOT_KEY'), log_level=logging.INFO)
ml = YCloudML(folder_id=os.getenv('GPT_FOLDER'), auth=os.getenv('GPT_API_KEY'))
model = ml.models.completions('yandexgpt').langchain(model_type="chat", timeout=60)

langchain = []

@yb.add_handler(command='/clear')
def clear_context(update: Update):
    global langchain
    langchain.clear()

@yb.add_handler(any=True)
def process_any(update: Update):
    global langchain
    langchain.append(HumanMessage(content=update.text))
    ai_message: AIMessage = model.invoke(langchain)
    langchain.append(ai_message)
    yb.send_message(ai_message.content, update)


if __name__ == "__main__":
    yb.start_pooling()
