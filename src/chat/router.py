import uuid
import os
import json
#from chat.database import insert_into_bd,start_bd
from http import cookies
import requests
from requests.auth import HTTPBasicAuth
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from huggingface_hub import InferenceClient



CLIENT_ID = os.getenv("CLIENT_ID")
SECRET = os.getenv("SBER_SECRET")
HF_TOKEN = os.getenv("HF_TOKEN")   
SC_TOKEN = os.getenv("SC_TOKEN")     
MIST_TOKEN = os.getenv("MIST_TOKEN")
GROQ_TOKEN = os.getenv("GROQ_TOKEN")

hist=[]

def ask_gpt(messages: str) -> str:
    pass
    
def ask_Mistral_7B_Instruct(messages: str) -> str:
    client = InferenceClient(
        "mistralai/Mistral-7B-Instruct-v0.2",
        token=HF_TOKEN,
    )
    answer = ""
    hist.append({"role": "user", "content": f"{messages}" })
    #insert_into_bd("user",messages,1)
    for message in client.chat_completion(
        messages=hist,
        max_tokens=9000,
        stream=True,
    ):
        answer+=message.choices[0].delta.content
    hist.append({"role": "assistant", "content": f"{answer}" })
    #insert_into_bd("assistant",answer,1)
    return answer

def ask_Mistral_Nemo_Instruct(messages: str) -> str:
    client = InferenceClient(
        "mistralai/Mistral-Nemo-Instruct-2407",
        token=HF_TOKEN,
    )
    answer = ""
    hist.append({"role": "user", "content": f"{messages}" })
    for message in client.chat_completion(
        messages=hist,
        max_tokens=9000,
        stream=True,
    ):
        answer+=message.choices[0].delta.content
    hist.append({"role": "assistant", "content": f"{answer}" })
    return answer

def ask_Mixtral_8x7B(messages: str) -> str:
    client = InferenceClient(
        "mistralai/Mixtral-8x7B-Instruct-v0.1",
        token=HF_TOKEN,
    )
    answer = ""
    hist.append({"role": "user", "content": f"{messages}" })
    for message in client.chat_completion(
        messages=hist,
        max_tokens=9000,
        stream=True,
    ):
        answer+=message.choices[0].delta.content
    hist.append({"role": "assistant", "content": f"{answer}" })
    return answer

def ask_Meta_Llama_3_1_70B_Instruct(messages: str) -> str:
    hist.append({"role": "user", "content": f"{messages}" })
    obj = json.loads((requests.post('https://api.sambanova.ai/v1/chat/completions', json={
        "model": "Meta-Llama-3.1-70B-Instruct",
        "messages": hist,
        "max_tokens": 1000
    }, headers={
        'Authorization': f'Bearer {SC_TOKEN}',
    }).content))
    try:
        hist.append({"role": "assistant", "content": f"{obj['choices'][0]['message']['content']}" })
        return obj['choices'][0]['message']['content']
    except Exception:
        print(obj)
        return 'Что то пошло не так'

def ask_Mixtral_8x22b(messages: str) -> str:
    hist.append({"role": "user", "content": f"{messages}" })
    obj = json.loads((requests.post('https://api.mistral.ai/v1/chat/completions', json={
        "model": "open-mixtral-8x22b",
        "messages": hist,
        "max_tokens": 1000
    }, headers={
        'Authorization': f'Bearer {MIST_TOKEN}',
    }).content))
    try:
        hist.append({"role": "assistant", "content": f"{obj['choices'][0]['message']['content']}" })
        return obj['choices'][0]['message']['content']
    except Exception:
        print(obj)
        return 'Что то пошло не так'

def ask_Gemma_7b(messages: str) -> str:
    hist.append({"role": "user", "content": f"{messages}" })
    obj = json.loads((requests.post('https://api.groq.com/openai/v1/chat/completions', json={
        "model": "gemma-7b-it",
        "messages": hist,
        "max_tokens": 1000
    }, headers={
        'Authorization': f'Bearer {GROQ_TOKEN}',
    }).content))
    try:
        hist.append({"role": "assistant", "content": f"{obj['choices'][0]['message']['content']}" })
        return obj['choices'][0]['message']['content']
    except Exception:
        print(obj)
        return 'Что то пошло не так'

def get_access_token() -> str:
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4()),
    }
    payload = {"scope": "GIGACHAT_API_PERS"}
    res = requests.post(
        url=url,
        headers=headers,
        auth=HTTPBasicAuth(CLIENT_ID, SECRET),
        data=payload,
        verify=False,
    )
    access_token = res.json()["access_token"]
    '''c = cookies.SimpleCookie()
    c["token"] = access_token
    print(c)'''
    return access_token

def send_prompt(msg: str, access_token: str):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
        "model": "GigaChat-Pro",
        "messages": [
            {
                "role": "user",
                "content": msg,
            }
        ],
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.post(url, headers=headers, data=payload, verify=False)
    return response.json()["choices"][0]["message"]["content"]

router = APIRouter(
    prefix="/ai/chat",
    tags=["Chat"]
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)


    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)




@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    manager = ConnectionManager()
    #start_bd()
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            value = await websocket.receive_text()
            await manager.send_personal_message(f"You: {data}", websocket)
            if value == "giga":
                await manager.send_personal_message(f"Assistent:\n {send_prompt(data, get_access_token())}", websocket)
            elif value == "chatgpt":
                await manager.send_personal_message(f"Assistent:\n {ask_gpt(data)}", websocket)
            elif value == "Mistral_7B_Instruct":
                await manager.send_personal_message(f"Assistent:\n {ask_Mistral_7B_Instruct(data)}", websocket)
            elif value == "Mistral_Nemo_Instruct":
                await manager.send_personal_message(f"Assistent:\n {ask_Mistral_Nemo_Instruct(data)}", websocket)
            elif value == "Mixtral_8x7B":
                await manager.send_personal_message(f"Assistent:\n {ask_Mixtral_8x7B(data)}", websocket)
            elif value == "Meta_Llama_3_1_70B_Instruct":
                await manager.send_personal_message(f"Assistent:\n {ask_Meta_Llama_3_1_70B_Instruct(data)}", websocket)
            elif value == "Mixtral_8x22b":
                await manager.send_personal_message(f"Assistent:\n {ask_Mixtral_8x22b(data)}", websocket)
            elif value == "Gemma_7b":
                await manager.send_personal_message(f"Assistent:\n {ask_Gemma_7b(data)}", websocket) 

    except WebSocketDisconnect:
        manager.disconnect(websocket)