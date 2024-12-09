import json
from channels.generic.websocket import AsyncWebsocketConsumer
#from chat.database import insert_into_bd,start_bd
from .utils import *

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


        message = data['message']              #сообщение
        language = data['language']            #выбранный язык
        value = data["value"]                  #выбранная модель
        #смена языка
        if self.old_language!= language:
            if language == "Русский":
                message+= ". Разговаривай со мной только по-русски"
            if language == "Français":
                message+= ". Communiquez avec moi uniquement en français"  #Общайся со мной только на французском языке
            if language == "English":
                message += ". Communicate with me only in English"   #Общайся со мной только на английском языке
            self.old_language = language

        await self.send(text_data=f"You: {message}")   #отправка сообщения пользователя

        if value == "Meta_Llama_3_1_70B_Instruct":
            response = await ask_Meta_Llama_3_1_70B_Instruct_async(message, self.client_id)
        elif value == "Mixtral_8x7B":
            response = await ask_Mixtral_8x7B_async(message, self.client_id)
        elif value == "Mixtral_8x22b":
            response = await ask_Mixtral_8x22b_async(message, self.client_id)
        elif value == "Gemma_7b":
            response = await ask_Gemma_7b_async(message, self.client_id)


        await self.send(text_data= f"Assistant: {response}")  #отправка ответа от ИИ


#       На случай возвращения старых моделей или добавлени я новых:
#       elif value == "chatgpt":
#       elif value == "Mistral_7B_Instruct":
#       elif value == "Mistral_Nemo_Instruct":
#       elif value == "Mixtral_8x22b":
