from enum import Enum
from telegram import Update
import json
import logger
import filehandler

#users that have been created
users: "dict[int, User]" = {}
#users waiting to be accepted
pending: "dict[int, str]" = {}
#blacklisted users
blacklisted: "dict[int, str]" = {}

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
        save_users()
        logger.info(self.name, f"{old_name} has changed username to '{new_name}'")

    def set_state(self, state: State): self.state = state

    def set_configured(self, configured: bool):
        self.configured = configured
        save_users()
        logger.info(self.name, "has been congigured")
    
    def set_joined(self, joined: bool, log=True):
        self.joined = joined
        save_users()
        if log:
            if joined:
                logger.info(self.name, "has joined to lottery")
            else:
                logger.info(self.name, "has canceled participation to lottery")

    def set_bot(self, bot_language: Language):
        self.bot_language = bot_language
        save_users()
        logger.info(self.name, f"has set bot language to {bot_language.name}")

    def set_lunch(self, lunch_language: Language):
        self.lunch_language = lunch_language
        save_users()
        logger.info(self.name, f"has set lunch language to {lunch_language.name}")

    def is_admin(self) -> bool:
        return (self.ID in filehandler.admins_ids())

#get user from given update
def get(update: Update) -> User:
    user = update.effective_user
    id = user.id
    try: return users[id]
    except KeyError: raise InvalidUser()
#add user to users
def add(id: int, name: str):
    users[id] = User(id, name)
    remove_pending(id)
    save_users()
    logger.info(name, "has been created")
#remove user from users
def remove(id: int):
    if id in users.keys():
        removed_user = users.pop(id)
        logger.info(removed_user.name, "removed from users")
#count joined users
def joined_users() -> "list[User]":
    return [user for user in users.values() if user.joined]

#set user waiting to be accepted
def set_pending(id: int, name: str):
    pending[id] = name
    logger.info(name, "is pending")
#remove user from waiting users
def remove_pending(id: int):
    if id in pending.keys(): pending.pop(id)
#blacklist user
def set_blacklisted(id: int, name: str):
    remove(id)
    remove_pending(id)
    blacklisted[id] = name
    logger.info(name, "is blacklisted")
#remove user from blacklisted users
def remove_blacklisted(id: int):
    if id in blacklisted.keys(): blacklisted.pop(id)

#save users to json-file
def save_users():
    def user_serialized(user: User):
        return {"name": user.name, "configured": user.configured, "joined": user.joined, 
                "bot": user.bot_language.name, "lunch": user.lunch_language.name}
    data = {id: user_serialized(user) for id, user in users.items()}
    open(filehandler.USERS_FP, "w").write(json.dumps(data, indent=2) )
#load user data from json-file
def load_users(test_fp: "str | None" =None):
    try:
        path = filehandler.USERS_FP if test_fp is None else test_fp
        data = json.load(open(path, "r"))
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

#exception that is raised when invalid user is trying to access bot
class InvalidUser(Exception):
    pass