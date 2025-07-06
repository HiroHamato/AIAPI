import requests
import json
from channels.generic.websocket import AsyncWebsocketConsumer
#from chat.database import insert_into_bd,start_bd
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoTest.settings')
django.setup()
from .models import ProgrammingLanguage, Prompt
from .utils import *
from asgiref.sync import sync_to_async
@sync_to_async
def getPromptText(prompt_id):
    try:
        return Prompt.objects.get(id=prompt_id).prompt_text
    except Prompt.DoesNotExist:
        return None
    except Exception as e:
        print(f"Database error: {str(e)}")
        return None
@sync_to_async
def getProgLng(language_id):
    try:
        return ProgrammingLanguage.objects.get(id=language_id).language_name
    except ProgrammingLanguage.DoesNotExist:
        return None
    except Exception as e:
        print(f"Database error: {str(e)}")
    return None
ADRESS = os.getenv("ADRESS")

proxies = {
            'http': os.getenv("PROXY"),
            'https': os.getenv("PROXY")
        }

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.client_id = self.scope['url_route']['kwargs']['client_id']
        if self.client_id not in hist:
            hist[self.client_id] = []
        self.old_language = None
        await self.accept()


    async def disconnect(self, close_code):
        if self.client_id in hist:
            del hist[self.client_id]
        print(f"Connection closed for client {self.client_id}")

    async def receive(self, text_data):
        data = json.loads(text_data)

        #Обработка нажатия кнопки Clear Context
        if data.get('action') == 'clear_context':
            hist[self.client_id] = []
            self.old_language = None
            await self.send(text_data="Context Cleared!")
            return

        type = data['type']
        message = data['message']              #сообщение
        language = data['language']            #выбранный язык
        value = data["value"]                  #выбранная модель       
        if self.old_language!= language:
            if language == "Русский":
                message+= ". Разговаривай со мной только по-русски"
            if language == "Français":
                message+= ". Communiquez avec moi uniquement en français"  #Общайся со мной только на французском языке
            if language == "English":
                message += ". Communicate with me only in English"   #Общайся со мной только на английском языке
            self.old_language = language
        if type == "2":
           progLng = await getProgLng(data['progLng'])
           promptText = await getPromptText(data['preprompt'])
           message = f"У меня есть задача по программированию, решай ее на языке {progLng}\n {message}"
           if not hasattr(self, 'last_prompt') or self.last_prompt != promptText:
               message += f". Препромпт: {promptText}"
               self.last_prompt = promptText
        if type == "3":
            progLng = await getProgLng(data['progLng'])
            code = data['code']
            promptText = await getPromptText(data['preprompt'])
            message = f"У меня есть задача по программированию, я написал для нее код на языке {progLng}, код не работает, найди пожалуйста ошибку. Задача: {message}. Код: {code}."
            if not hasattr(self, 'last_prompt') or self.last_prompt != promptText:
                message+=f". Препромпт: {promptText}"
                self.last_prompt = promptText
        await self.send(text_data=f"You: {message}")   #отправка сообщения пользователя

        if value == "Meta_Llama_3_1_70B_Instruct":
            response = await ask_Meta_Llama_3_1_70B_Instruct_async(message, self.client_id)
        elif value == "Mixtral_8x7B":
            response = await ask_Mixtral_8x7B_async(message, self.client_id)
        elif value == "Mixtral_8x22b":
            response = await ask_Mixtral_8x22b_async(message, self.client_id)
        elif value == "DeepSeek_R1_Distill_Llama_70B":
            response = await ask_DeepSeek_R1_Distill_Llama_70B_async(message, self.client_id)
        elif value == "Llama_3_1_Tulu_3_405B":
            response = await ask_Llama_3_1_Tulu_3_405B_async(message, self.client_id)
        elif value == "DeepSeek_R1":
            response = await ask_DeepSeek_R1_async(message, self.client_id)
        elif value == "QwQ_32B":
            response = await ask_QwQ_32B_async(message, self.client_id)


        await self.send(text_data= f"Assistant: {response}")  #отправка ответа от ИИ


#       На случай возвращения старых моделей или добавлени я новых:
#       elif value == "chatgpt":
#       elif value == "Mistral_7B_Instruct":
#       elif value == "Mistral_Nemo_Instruct":
#       elif value == "Mixtral_8x22b":


