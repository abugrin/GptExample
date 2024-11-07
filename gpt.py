import logging
import os
from dotenv import load_dotenv
from yambot import MessengerBot
from yambot.types import Update
from yandex_cloud_ml_sdk import YCloudML
from langchain_core.messages import AIMessage, HumanMessage

load_dotenv()
yb = MessengerBot(os.getenv('BOT_KEY'), log_level=logging.DEBUG)
ml = YCloudML(folder_id=os.getenv('GPT_FOLDER'), auth=os.getenv('GPT_API_KEY'))
model = ml.models.completions('yandexgpt').langchain(model_type="chat", timeout=60)

lang_chains = {}

@yb.add_handler(command='/clear')
def clear_context(update: Update):
    global lang_chains
    lang_chains.pop(f'{update.from_m.from_id}')
    yb.send_message(f'Context cleared for user {update.from_m.login}', update)

@yb.add_handler(any=True)
def process_any(update: Update):
    global lang_chains
    lang_chain = lang_chains.get(f'{update.from_m.from_id}')

    if not lang_chain:
        lang_chain = {f'{update.from_m.from_id}': [HumanMessage(content=update.text)]}
        lang_chains.update(lang_chain)
    else:
        lang_chains[f'{update.from_m.from_id}'].append(HumanMessage(content=update.text))

    ai_message: AIMessage = model.invoke(lang_chains[f'{update.from_m.from_id}'])
    lang_chains[f'{update.from_m.from_id}'].append(ai_message)
    yb.send_message(ai_message.content, update)


if __name__ == "__main__":
    yb.start_pooling()
