from pydantic import BaseModel
from typing import List
from enum import Enum
from openai import OpenAI, AsyncOpenAI
import random
import pandas as pd
import numpy as np
import time
import asyncio as aio

from schemas import *

from openai_interface import *
from user import User

# classe de mensagens do role: user


# classe de mensagens do estilo gpt, o content é obtido pelo Message.content

#todo: implementar a logica de achar uma cidade mais apropriadamente







user_list = {}
favorite_messages = {}


# banco de dados de usuarios (provisorio)
user_list = {"André" : User(username="André", message_history=[GptMessage(role="user", content="Se estou lendo isso, é porque deu certo")])}

#exemplo#
rob = User(username="Robinson", message_history=[])
rob.addMessage(Message(username="robinser", content="eae"))
#print(rob.message_history)
