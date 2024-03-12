import telegram
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, CommandHandler, filters, MessageHandler, CallbackQueryHandler
import commands
import userconfig
import user
from user import Language, State
import messages
import logger

#handle user message
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _user = user.get(update)
    ans = update.message.text.lower()
    #reply when user is in default state
    if _user.state == State.START:
        await update.message.reply_text(messages.NOT_COMMAND.get(_user))
    #handle answer to bot language question
    elif _user.state == State.Q1:
        async def set_lang(lang: Language):
            _user.set_bot(lang)
            await userconfig.progress(update, context)
        if 'suomea' in ans or 'finnish' in ans:
            await set_lang(Language.FIN)
        elif 'englantia' in ans or 'english' in ans:
            await set_lang(Language.ENG)
        else: 
            await update.message.reply_text(messages.reply_not_valid(ans).get(_user))
    #handle answer to lunch language question
    elif _user.state == State.Q2:
        async def set_lang(lang: Language):
            _user.set_lunch(lang)
            await update.message.reply_text(messages.LUNCH_LANGUAGE[lang.value].get(_user), reply_markup=ReplyKeyboardRemove())
            await userconfig.progress(update, context)
        if 'suomea' in ans or 'finnish' in ans:
            await set_lang(Language.FIN)
        elif 'englantia' in ans or 'english' in ans:
            await set_lang(Language.ENG)
        elif 'ei väliä' in ans or 'no preference' in ans:
            await set_lang(Language.BOTH)
        else: 
            await update.message.reply_text(messages.reply_not_valid(ans).get(_user))

#handles callback querys for accepting users
async def user_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    if data is not None:
        accepted = int(data[:1])
        id = int(data[1:])
        name = user.pending[id]
        if accepted:
            user.add(id, name)
            txt = name + " accepted."
            await context.bot.send_message(id, "You have been accepted! Tell me now your /preferences.")
        else:
            user.set_blacklisted(id, name)
            txt = name + " declined."
        await update.callback_query.edit_message_text(txt)
    
#handle errors
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    if isinstance(context.error, user.InvalidUser):
        pass
    elif isinstance(context.error, telegram.error.NetworkError) & (not isinstance(context.error, telegram.error.BadRequest)):
        error_msg = "NetworkError: Connection error occurred"
        if not error_msg in logger.last_log():
            logger.error(error_msg)
    else:
        logger.exception(f"{context.error}")

#command handlers
HANDLERS = (
    CommandHandler("start", commands.start), 
    CommandHandler(["komennot", "commands"], commands.commands),
    CommandHandler(["mieltymykset", "preferences"], commands.preferences),
    CommandHandler(["tietoa", "info"], commands.info),
    CommandHandler(["liity", "join"], commands.join),
    CommandHandler(["peru", "cancel"], commands.cancel),
    CommandHandler(["lotto", "lottery"], commands.lottery_cmd),
    CommandHandler("schedule_lottery", commands.schedule_lottery),
    CommandHandler("pause_lottery", commands.pause_lottery),
    CommandHandler("start_lottery", commands.start_lottery),
    CommandHandler("get_log", commands.get_log),
    CallbackQueryHandler(user_query),
    MessageHandler(filters.TEXT, message_handler))
