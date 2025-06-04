import os

estrutura = {
    "iot-monitoring": {
        "api": {
            "main.py": '''\
from fastapi import FastAPI, WebSocket
from pymongo import MongoClient
import os

app = FastAPI()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["iot"]
collection = db["data"]

@app.post("/data")
async def post_data(payload: dict):
    collection.insert_one(payload)
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        await ws.send_text("ping")
''',
        },
        "sensor_simulator": {
            "simulate.py": '''\
import asyncio
import random
import aiohttp

URL = "https://sua-api.render.com/data"

async def send_data(sensor_id):
    while True:
        data = {
            "sensor_id": sensor_id,
            "temperature": round(random.uniform(20, 35), 2),
            "humidity": round(random.uniform(30, 70), 2)
        }
        async with aiohttp.ClientSession() as session:
            await session.post(URL, json=data)
        await asyncio.sleep(5)

async def main():
    tasks = [send_data(f"sensor_{i}") for i in range(5)]
    await asyncio.gather(*tasks)

asyncio.run(main())
''',
        },
        "dashboard": {
            "pages": {
                "index.js": '''\
import { useEffect, useState } from 'react';

export default function Dashboard() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    const socket = new WebSocket("wss://sua-api.render.com/ws");
    socket.onmessage = (event) => setMessage(event.data);
  }, []);

  return <div>Mensagem em tempo real: {message}</div>;
}
'''
            }
        },
        ".env": "MONGO_URI=mongodb+srv://<usuario>:<senha>@cluster.mongodb.net/?retryWrites=true&w=majority",
        "README.md": "# IoT Monitoring Project\n\nSistema distribuído para monitoramento com IoT, FastAPI, MongoDB, e Next.js."
    }
}

def criar_estrutura(base, estrutura):
    for nome, conteudo in estrutura.items():
        caminho = os.path.join(base, nome)
        if isinstance(conteudo, dict):
            os.makedirs(caminho, exist_ok=True)
            criar_estrutura(caminho, conteudo)
        else:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(conteudo)

# Executa
if __name__ == "__main__":
    criar_estrutura(".", estrutura)
    print("Projeto 'iot-monitoring' criado com sucesso!")
