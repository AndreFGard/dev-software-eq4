from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi import staticfiles, Body
from typing import List
import model as m
import uvicorn
import os
import sys
import asyncio

import user

if ("fastapi" not in  sys.argv[0] and "uvicorn" not in sys.argv[0]): 
    print("\n\t🦄🦄🦄🦄🦄🦄🦄🦄\033[1;31m Please run this file with 'fastapi run dev'")


from schemas import Activity, GPTMessage, LLMModelInfo, Schedule
class Settings(BaseSettings):
    OPENAI_KEY: str = ''
    BRAVE_KEY: str = ''
    TEMBO_PSQL_URL: str = ''
    HIGH_LIMIT_MODELS: list[LLMModelInfo] = []

    model_config = SettingsConfigDict(env_nested_delimiter='__', env_file='.env')


settings=Settings()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_model = LLMModelInfo(url="https://api.groq.com/openai/v1",
                model="gemma2-9b-it",
                rate_limit=8000,
                key=settings.OPENAI_KEY) if settings.OPENAI_KEY else None

openai = m.userOpenai(
                    main_model=main_model,
                    cheap_models=settings.HIGH_LIMIT_MODELS,
                    brave_api_key=settings.BRAVE_KEY,
                    TEMBO_PSQL_URL=settings.TEMBO_PSQL_URL)

@app.on_event("startup")
async def startup_event():
    await openai.RAG.db._create_tables()

@app.get("/")
async def root():
    return "Please access index.html"


from model import UserDB
userdb = UserDB()

@app.post("/addMessage")
@app.post("/addData")
async def addMessage(msg: m.Message):
    """Recebe uma mensagem nova, determina o usuario, pega a resposta 
    de uma IA, adiciona no historico de mensagens
    e retorna o historico de mensagens"""

    username = msg.username
    user = userdb.getUser(username)
    user.addMessage(msg)
    reply = await openai.reply(user)
    user.addMessage(m.Message(username="assistant", content=reply ))
    messages =user.getMessageHistory()

    return messages

addData = addMessage 

@app.get("/getMessages", response_model=List[m.Message])
async def getMessages(username:str) -> List[m.Message]:
    """"retorna as mensagens relativas a um usuário (mesmo que seja o usuario padrão)
    Essa função devera receber o nome de usuario em um campo separado do json"""

    return userdb.getUser(username).getMessageHistory()

@app.post('/addToFavorites', response_model=List[Activity])
async def addToFavorites(username: str = Body(...), id: int = Body(...)) -> list[Activity]:
    """Adiciona uma mensagem aos favoritos de um usuário"""
    msg: GptMessage = userdb.getMessageById(username, id) #type: ignore
    userdb.addActivitiy(username, m.Activity(name="Act name", short_description=msg.content, long_description=msg.content))
    return userdb.getActivities(username)

@app.post('/removeFavorite', response_model=List[Activity])
async def remove_favorite(username: str = Body(...), id: int = Body(...)) ->list[Activity]:
    """Remove uma mensagem dos favoritos de um usuário"""
    try:
        userdb.deleteAcitivty(username, id)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to remove activity")

    return  userdb.getActivities(username)

@app.get('/getFavorites', response_model=List[Activity])
async def getFavorites(username: str) -> list[Activity]:
    """Retorna as mensagens favoritas de um usuário"""

    return userdb.getActivities(username)


@app.get('/getSchedule',)
async def getSchedule(username: str) -> Schedule | None:
    try:
        sched = userdb.getSchedule(username)
        if not sched: print(f"No schedule found for user {username}")
        return sched
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to get schedule, user likely not in the database")

@app.post('/createSchedule', response_model=Schedule)
async def makeSchedule(username: str):
    try:
        sched = await openai.make_schedule(userdb.getUser(username), userdb.getActivities(username))
        if sched:
            userdb.addSchedule(username, sched)
        return sched
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to generate schedule")



if os.path.exists('frontend/dist'):
    app.mount("/", staticfiles.StaticFiles(directory="frontend/dist", html=True), name="static")
else:
    print("Not serving static files, please build them")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
