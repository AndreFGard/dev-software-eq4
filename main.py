import model as m
import uvicorn
import os
import sys

from user import User
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from fastapi import staticfiles, Body
from typing import List

if ("fastapi" not in  sys.argv[0] and "uvicorn" not in sys.argv[0]): 
    print("\n\t🦄🦄🦄🦄🦄🦄🦄🦄\033[1;31m Please run this file with 'fastapi run dev'")


class Settings(BaseSettings):
    OPENAI_KEY: str = ''
    BRAVE_KEY: str = ''
    TEMBO_PSQL_URL: str = ''
    class Config:
        env_file = ".env"

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

# @app.post("/addMessage")
# @app.post("/addData")
# async def addData(msg: m.Message):
#     """Recebe uma mensagem nova, determina o usuario, pega a resposta 
#     de uma IA e adiciona no historico de mensagens
#     e retorna o historico de mensagens"""
#     #preencher aqui
#     if (msg.username not in m.user_list):
#         user = m.User(msg.username)
#         m.user_list[msg.username] = user
#     else:
#         user = m.user_list[msg.username]
#     await user.add_message(msg)
#     reply = await openai.reply(user)
#     await user.add_message(m.Message(username="assistant", content=reply ))
#     messages =user.get_message_history()
#     return messages

@app.post("/addMessage")
@app.post("/addData")
async def add_message(msg: m.Message):
    """Adiciona uma mensagem ao histórico do usuário."""
    user = User(username=msg.username)
    await user.load()
    await user.add_message(msg)
    return {"status": "Message added successfully"}

# @app.get("/getMessages", response_model=List[m.Message])
# async def getMessages(username:str) -> List[m.Message]:
#     """"retorna as mensagens relativas a um usuário (mesmo que seja o usuario padrão)
#     Essa função devera receber o nome de usuario em um campo separado do json"""

#     if username not in m.user_list.keys():
#         m.user_list[username] = m.User(username=username)

#     return m.user_list[username].getMessageHistory()

@app.get("/getMessages", response_model=List[m.Message])
async def get_messages(username: str) -> List[m.Message]:
    """"retorna as mensagens relativas a um usuário (mesmo que seja o usuario padrão)"""

    user = User(username=username)
    await user.load()

    return await user.get_message_history()

# @app.post('/addToFavorites', response_model=List[m.Message])
# async def addToFavorites(username: str = Body(...), msg: m.Message = Body(...)):
#     if username not in m.favorite_messages: m.favorite_messages[username] = {msg.id: msg}
#     else: m.favorite_messages[username][msg.id] = msg
#     return list(m.favorite_messages[username].values())

@app.post("/addToFavorites")
async def add_to_favorites(username: str = Body(...), msg: m.Message = Body(...)):
    """adiciona uma mensagem à lista de favoritos de um usuário"""
    user = User(username=username)
    await user.load()
    await user.add_to_favorites(msg)
    return {"status": "Message added to favorites"}

# @app.get('/getFavorites', response_model=List[m.Message])
# async def getFavorites(username: str):
#     if username not in m.favorite_messages: return []
#     return m.favorite_messages[username]

@app.get("/getFavorites", response_model=List[m.Message])
async def get_favorites(username: str) -> List[m.Message]:
    """retorna as mensagens favoritadas de um usuário"""

    user = User(username=username)
    await user.load()

    return await user.get_favorites()

if os.path.exists('frontend/dist'):
    app.mount("/", staticfiles.StaticFiles(directory="frontend/dist", html='True'), name="static")
else:
    print("Not serving static files, please build them")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
