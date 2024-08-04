import uuid
import json
from http import cookies
import requests
from requests.auth import HTTPBasicAuth
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from huggingface_hub import InferenceClient


CLIENT_ID = "f732e32a-db6c-478b-b49e-5fa94bdfe939"
SECRET = "acb87642-5f71-4cc2-9861-b756fbe2a681"
HF_TOKEN = "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"

def ask_gpt(messages: str) -> str:
    pass
    
def ask_Mistral_7B_Instruct(messages: str) -> str:
    client = InferenceClient(
        "mistralai/Mistral-7B-Instruct-v0.2",
        token=HF_TOKEN,
    )
    answer = ""
    for message in client.chat_completion(
        messages=[{"role": "user", "content": f"{messages}" }],
        max_tokens=9000,
        stream=True,
    ):
        answer+=message.choices[0].delta.content
    return answer

def ask_gemma_2b_it(messages: str) -> str:
    client = InferenceClient(
        "google/gemma-2b-it",
        token=HF_TOKEN,
    )
    answer = ""
    for message in client.chat_completion(
        messages=[{"role": "user", "content": f"{messages}" }],
        max_tokens=9000,
        stream=True,
    ):
        answer+=message.choices[0].delta.content
    return answer

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


manager = ConnectionManager()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            value = await websocket.receive_text()
            await manager.send_personal_message(f"You: {data}", websocket)
            if value == "giga":
                await manager.send_personal_message(f"Assistent: {send_prompt(data, get_access_token())}", websocket)
            elif value == "chatgpt":
                await manager.send_personal_message(f"Assistent: {ask_gpt(data)}", websocket)
            elif value == "Mistral_7B_Instruct":
                await manager.send_personal_message(f"Assistent: {ask_Mistral_7B_Instruct(data)}", websocket)
            elif value == "gemma_2b_it":
                await manager.send_personal_message(f"Assistent: {ask_gemma_2b_it(data)}", websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
