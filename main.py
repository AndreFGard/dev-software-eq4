from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from fastapi import staticfiles, Body
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
    #preencher aqui
    if (msg.username not in m.user_list):
        user = m.User(msg.username)
        m.user_list[msg.username] = user
    else:
        user = m.user_list[msg.username]
    user.addMessage(msg)
    reply = await openai.reply(user)
    user.addMessage(m.Message(username="assistant", content=reply ))
    messages =user.getMessageHistory()
    return messages

@app.get("/getMessages", response_model=List[m.Message])
async def getMessages(username:str) -> List[m.Message]:
    """"retorna as mensagens relativas a um usuário (mesmo que seja o usuario padrão)
    Essa função devera receber o nome de usuario em um campo separado do json"""

    if username not in m.user_list.keys():
        m.user_list[username] = m.User(username=username)

    return m.user_list[username].getMessageHistory()

@app.post('/addToFavorites', response_model=List[m.Message])
async def addToFavorites(username: str = Body(...), msg: m.Message = Body(...)):
    if username not in m.favorite_messages: m.favorite_messages[username] = [msg]
    else: m.favorite_messages[username].append(msg)
    return m.favorite_messages[username]

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
