from typing import List
from bot import runBot

class User:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name

class Users:
    def __init__(self, users: List[User]):
        self.users = users

if __name__ == '__main__':
    runBot()
