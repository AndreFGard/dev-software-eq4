from fastapi import FastAPI, HTTPException, Body, staticfiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from database.connection import Database
from schemas import Activity, GPTMessage, LLMModelInfo, Schedule, message_to_gpt_message
from user import User
from database.session import db
import model as m
import uvicorn
import os
import sys
import asyncio

import user

if ("fastapi" not in  sys.argv[0] and "uvicorn" not in sys.argv[0]): 
    print("\n\t🦄🦄🦄🦄🦄🦄🦄🦄\033[1;31m Please run this file with 'fastapi run dev'")

class Settings(BaseSettings):
    OPENAI_KEY: str = ''
    BRAVE_KEY: str = ''
    TEMBO_PSQL_URL: str = ''
    HIGH_LIMIT_MODELS: list[LLMModelInfo] = []

    model_config = SettingsConfigDict(env_nested_delimiter='__', env_file='.env')


asyncio.run(db.async_main())

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
    from rag.rag import crawler
    await crawler.start()


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

    user = await User.get_or_create(msg.username)
    await user.addMessage(msg)
    reply = await openai.reply(user)
    await user.addMessage(m.Message(username="assistant", content=reply))
    return await user.getMessageHistory()

@app.get("/getMessages", response_model=List[m.Message])
async def getMessages(username:str) -> List[m.Message]:
    """"retorna as mensagens relativas a um usuário (mesmo que seja o usuario padrão)
    Essa função devera receber o nome de usuario em um campo separado do json"""

    user = await User.get_or_create(username)
    return await user.getMessageHistory()

@app.post('/addToFavorites', response_model=List[Activity])
async def addToFavorites(username: str = Body(...), id: int = Body(...)) -> list[Activity]:
    """Adiciona uma mensagem aos favoritos de um usuário"""

    user = await User.get_or_create(username)
    msg = await user.getMessageById(id)
    if msg is None:
        raise HTTPException(status_code=404, detail="Message not found")
    await user.addActivity(msg)
    return await user.getActivities()

@app.post('/removeFavorite', response_model=List[Activity])
async def remove_favorite(username: str = Body(...), id: int = Body(...)) ->list[Activity]:
    """Remove uma mensagem dos favoritos de um usuário"""
    try:
        user = await User.get_or_create(username)
        await user.removeActivity(id)
        return await user.getActivities()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to remove activity")

@app.get('/getFavorites', response_model=List[Activity])
async def getFavorites(username: str) -> list[Activity]:
    """Retorna as mensagens favoritas de um usuário"""

    user = await User.get_or_create(username)
    return await user.getActivities()


@app.post('/updateFavorite', response_model=List[Activity])
async def update_favorite(username: str = Body(...), id: int = Body(...), activity: Activity = Body(...)) -> list[Activity]:
    """Atualiza uma mensagem favorita de um usuário"""
    try:
        user = await User.get_or_create(username)
        await user.updateActivity(id, activity)
        return await user.getActivities()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to update activity")

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

# import auth
# app.include_router(auth.router, prefix="/auth", tags=["authentication"])

if os.path.exists('frontend/dist'):
    app.mount("/", staticfiles.StaticFiles(directory="frontend/dist", html=True), name="static")
else:
    print("Not serving static files, please build them")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
