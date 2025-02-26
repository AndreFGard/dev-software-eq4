from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from fastapi import staticfiles, Body
from start import db
from typing import List
import model as m
import uvicorn
import os
import sys

if ("fastapi" not in  sys.argv[0] and "uvicorn" not in sys.argv[0]): 
    print("\n\t🦄🦄🦄🦄🦄🦄🦄🦄\033[1;31m Please run this file with 'fastapi run dev'")


class Settings(BaseSettings):
    OPENAI_KEY: str = ''

settings=Settings()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = m.user_list
openai = m.OpenaiInteface(useDummy=not settings.OPENAI_KEY,openai_key=settings.OPENAI_KEY)
print(settings.OPENAI_KEY)

@app.get("/")
async def root():
    return "Please access index.html"

messagesyet=[]

@app.post("/addMessage")
@app.post("/addData")
async def addData(msg: m.Message):
    """Recebe uma mensagem nova, determina o usuario, pega a resposta 
    de uma IA e adiciona no historico de mensagens
    e retorna o historico de mensagens"""

    try:
        user_data = {"username": msg.username, "password" : "senha"}
        user_exists = await db.read_data("users", user_data)

        if not user_exists:
            await db.add_data("users", user_data)

        await db.add_data("messages", {"content_message": msg.dict()})

        reply = await openai.reply(msg)
        assistant_msg = m.Message(username="assistant", content=reply)
        await db.add_data("messages", {"content_message": assistant_msg.dict()})

        messages = await db.read_data("messages", {"username" : msg.username})

        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/getMessages", response_model=List[m.Message])
async def getMessages(username: str) -> List[m.Message]:
    """"retorna as mensagens relativas a um usuário (mesmo que seja o usuario padrão)
    Essa função devera receber o nome de usuario em um campo separado do json"""
    try:
        user_data = {"username": username}
        user_exists = await db.read_data("USERS", user_data)
        
        if not user_exists:
            await db.add_data("USERS", user_data)
        
        messages = await db.read_data("MESSAGES", {"username": username})
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/addToFavorites', response_model=List[m.Message])
async def addToFavorites(username: str = Body(...), msg: m.Message = Body(...)):
    if username not in m.favorite_messages: m.favorite_messages[username] = {msg.id: msg}
    else: m.favorite_messages[username][msg.id] = msg
    return list(m.favorite_messages[username].values())

@app.get('/getFavorites', response_model=List[m.Message])
async def getFavorites(username: str):
    if username not in m.favorite_messages: return []
    return m.favorite_messages[username]

if os.path.exists('frontend/dist'):
    app.mount("/", staticfiles.StaticFiles(directory="frontend/dist", html='True'), name="static")
else:
    print("Not serving static files, please build them")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
