from fastapi import FastAPI
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import model as m
import uvicorn
import os
import sys

class Settings(BaseSettings):
    PORT: int = 8000
    openrouter_key: str = ""

settings = Settings()

if ("fastapi" not in  sys.argv[0] and "uvicorn" not in sys.argv[0]): 
    print("\n\t🦄🦄🦄🦄🦄🦄🦄🦄\033[1;31m Please run this file with 'fastapi run dev'")


app = FastAPI()

origins = [
    "http://localhost:5173", 
    os.getenv("FRONTEND_URL", "https://production.com") 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = m.user_list
openai = m.OpenaiInteface(openai_key=settings.openai_key, useDummy=True)


@app.get("/")
async def root():
    return {"message": "Hello World"}

messagesyet=[]

@app.post("/addMessage")
@app.post("/addData")
async def addData(msg: m.Message):
    """Recebe uma mensagem nova, determina o usuario, pega a resposta 
    de uma IA e adiciona no historico de mensagens
    e retorna o historico de mensagens"""
    #preencher aqui
    messages =[msg]
    messages.append(m.Message(username="fakegpt", content=openai.getReply()))
    return messages

@app.post("/getMessages", response_model=List[m.GptMessage])
async def getMessages(username:str) -> List[m.GptMessage]:
    """"retorna as mensagens relativas a um usuário (mesmo que seja o usuario padrão)
    Essa função devera receber o nome de usuario em um campo separado do json"""
    pass




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=settings.PORT)