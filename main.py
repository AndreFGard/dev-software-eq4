from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import model as m
import uvicorn
import os
import sys

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



@app.get("/")
async def root():
    return {"message": "Hello World"}

messagesyet=[]

@app.post("/addData")
async def addData(msg: m.Message):
    """Recebe uma mensagem nova, determina o usuario, pega a resposta 
    de uma IA e adiciona no historico de mensagens
    e retorna o historico de mensagens"""
    #preencher aqui
    messages =["eae"]
    return messages





if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)