from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import messages
import user
from user import State, User, Language
import lottery
import logger

class Keyboard:
    def __init__(self, keyboard_fin: "list[list[str]]", keyboard_eng: "list[list[str]]"):
        self.FIN = keyboard_fin
        self.ENG = keyboard_eng

    def get(self, _user: User) -> "list[list[str]]":
        if _user.bot_language == Language.FIN:
            return self.FIN
        else:
            return self.ENG

BOT_LANGUAGE_KB = Keyboard([['Suomea', 'Englantia']], [['Finnish', 'English']])
LUNCH_LANGUAGE_KB = Keyboard([['Suomea', 'Englantia', 'Ei väliä']], [['Finnish', 'English', 'No preference']])

#function that is called when user-configuration progresses
async def progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _user = user.get(update)
    if _user.state == State.Q2:
        #user config completed
        if not _user.configured:
            #check that user config did not fail
            if (_user.bot_language is not Language.NONE) & (_user.lunch_language is not Language.NONE):
                await context.bot.send_message(_user.ID, messages.CONFIGURED.get(_user))
                _user.set_configured(True)
                #send lunch lottery notification to user if active lottery
                if lottery.is_active():
                    await context.bot.send_message(_user.ID, messages.lottery_noti().get(_user))
                    logger.info(None, f"Lottery notification has been sent to user {_user.name}")
            else: await context.bot.send_message(_user.ID, messages.CONFIG_FAILED.get(_user))
        _user.set_state(State.START)
    else:
        #bot language config
        if _user.state == State.START:
            question = messages.BOT_LANGUAGE
            keyboard = BOT_LANGUAGE_KB
            _user.set_state(State.Q1)
        #lunch language config
        else:
            #send welcome message to users not yet configured
            if not _user.configured:
                await context.bot.send_message(_user.ID, messages.WELCOME.get(_user))
            question = messages.LUNCH_LANGUAGE[0]
            keyboard = LUNCH_LANGUAGE_KB
            _user.set_state(State.Q2)
        reply_markup = ReplyKeyboardMarkup(keyboard.get(_user), resize_keyboard=True, one_time_keyboard=True, input_field_placeholder=question.get(_user))
        await update.message.reply_text(question.get(_user), reply_markup=reply_markup)