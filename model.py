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

from userOpenai import *
from user import User

user_list = {}
favorite_messages = {}

# banco de dados de usuarios (provisorio)
user_list = {"André" : User(username="André", message_history=[GptMessage(role="user", content="Se estou lendo isso, é porque deu certo")])}

