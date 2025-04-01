
from schemas import *
class User:
    def __init__(self, username="John Doe"):
        self.username = username
        self.status = UserStatus.DISCUSSING

    def __repr__(self):
        return f"User(username={self.username}, status={self.status})"