from pydantic import BaseModel
from typing import List
import openai
import random

class Message(BaseModel):
    username: str
    content: str

class GptMessage(BaseModel):
    role: str
    content: str

#todo: implementar a logica de achar uma cidade mais apropriadamente
class City:
    name:str

def answerDummy(*args, **kwargs):
    buzzwords = [ "Dev Software", "Concepcao de artefatos", "????", "Forms", "Eigenvalues "
    "synergy", "pivot", ",", "mas também", "blockchain", ", além de ", "cloud-native", ".",
    "big data",]
    return " ".join(random.sample(buzzwords, 3) )

user_list = {}
class OpenaiInteface:
    """Essa classe proverÁ (quando isso for implementado) 
    as respostas de um chatbot.
    Essa classe deve preparar os parametros, prompts e outras coisas
    Parameters:
    useDummy (bool): usar um chatbot fake ou não;."""
    def __init__(self, useDummy=True, **kwargs):
        self.openai = None
        self.getReply = answerDummy
        if (useDummy):
            #nao usar o chatgpt de verdade
            self.openai = None
        else:
            #inicializar o modulo openai
            #implementar aqui
            pass


class User():
    username: str
    message_history: List[GptMessage]
    def __init__(self, username="John Doe", message_history=[]):
        self.username = username
        self.message_history = message_history
    def addMessage(self, msg: Message):
        role = "assistant"
        if msg.username != "assistant":
            role = "user"
        self.message_history.append(GptMessage(role=role, content = msg.content))
    
    def getMessageHistory(self) -> List[Message]:
        return [Message(username= self.username if item.role == "user" else "assistant", content=item.content) for item in self.message_history]
    


#exemplo#
rob = User(username="Robinson", message_history=[])
rob.addMessage(Message(username="robinser", content="eae"))
#print(rob.message_history)
