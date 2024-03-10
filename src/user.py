from enum import Enum
from telegram import Update
import json
import logger

class State(Enum):
    START = 0
    Q1 = 1
    Q2 = 2

class Language(Enum):
    NONE = 0
    FIN = 1
    ENG = 2
    BOTH = 3

class User:
    def __init__(self, id: int, name: str):
        self.ID = id
        self.name = name
        self.state: State = State.START
        self.configured: bool = False
        self.joined: bool = False
        self.bot_language: Language = Language.NONE
        self.lunch_language: Language = Language.NONE

    def update_name(self, new_name: str):
        old_name = self.name
        self.name = new_name
        save_users(USERS_FP)
        logger.info(self.name, f"{old_name} has changed username to '{new_name}'")

    def set_configured(self, configured: bool):
        self.configured = configured
        save_users(USERS_FP)
        logger.info(self.name, "has been congigured")
    
    def set_joined(self, joined: bool, log=True):
        self.joined = joined
        save_users(USERS_FP)
        if log:
            if joined:
                logger.info(self.name, "has joined to lottery")
            else:
                logger.info(self.name, "has canceled participation to lottery")

    def set_bot(self, bot_language: Language):
        self.bot_language = bot_language
        save_users(USERS_FP)
        logger.info(self.name, f"has set bot language to {bot_language.name}")

    def set_lunch(self, lunch_language: Language):
        self.lunch_language = lunch_language
        save_users(USERS_FP)
        logger.info(self.name, f"has set lunch language to {lunch_language.name}")

    def is_admin(self) -> bool:
        with open('files/admins.txt', 'r') as file:
            ids = [line.strip() for line in file]
            return (str(self.ID) in ids)

#filepath for users file
USERS_FP = "files/users.json"

#users that are subscribed to the bot
users: dict[int, User] = {}

#get user from given update
def get(update: Update) -> User:
    update_user = update.effective_user
    if update_user.id in users:
        return users[update_user.id]
    else:
        users[update_user.id] = User(update_user.id, update_user.name)
        save_users(USERS_FP)
        logger.info(update_user.name, "has been created")
        return users[update_user.id]

#remove user from users
def remove(user_id: int):
    if user_id in users.keys():
        removed_user = users.pop(user_id)
        logger.info(removed_user.name, "removed from users")

#count joined users
def joined_count() -> int:
    return sum(1 for user in users.values() if user.joined)

#serialize user object into json-format
def user_serialized(user: User):
    return {
    "name": user.name,
    "configured": user.configured, 
    "joined": user.joined, 
    "bot": user.bot_language.name, 
    "lunch": user.lunch_language.name}

#save users to json-file
def save_users(path: str):
    data = {id: user_serialized(user) for id, user in users.items()}
    js = json.dumps(data, indent=2) 
    fp = open(path, "w")
    fp.write(js)
    fp.close()
    
#load user data from json-file
def load_users(path: str):
    try:
        fp = open(path, "r")
        data = json.load(fp)
        fp.close()
        ids = data.keys()
        #for each saved user make user object and add it to users
        for id in ids:
            id_int = int(id)
            user = User(id_int, data[id]["name"])

            user.configured = data[id]["configured"]
            user.joined = data[id]["joined"]
            user.bot_language = Language[data[id]["bot"]]
            user.lunch_language = Language[data[id]["lunch"]]

            users[id_int] = user
        logger.info(None, f"{len(ids)} user(s) loaded from '{path}'")
    except KeyError:
        logger.error("KeyError: User data is corrupted")
    except json.decoder.JSONDecodeError:
        logger.error(f"JSONDecodeError: Tried to load users from '{path}' but the file was empty")
