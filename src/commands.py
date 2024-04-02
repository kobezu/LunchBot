from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
import user
import userconfig
import messages
import lottery
import callbacks
import filehandler
import random

#command to start bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    #check that user is not in users
    if (u.id not in user.users):
        #check if user is admin
        if (u.id in filehandler.admins_ids()): 
            user.add(u.id, u.name)
            await preferences(update, context)
        #check that user has not interacted with the bot before
        elif (u.id not in user.blacklisted) & (u.id not in user.pending):
            user.set_pending(u.id, u.name)
            await update.message.reply_text("An approval request has been send to the bot admin. Please wait until you are accepted.")
            admin_id = filehandler.admins_ids()[0] 
            kb = [[InlineKeyboardButton(text="Accept", callback_data=f"1{u.id}"), 
                InlineKeyboardButton(text="Decline", callback_data=f"0{u.id}")]]
            await context.bot.send_message(admin_id, f"User pending: {u.name}", reply_markup=InlineKeyboardMarkup(kb))
    else: await preferences(update, context)

#command to get list of commands
async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _user = user.get(update)
    msg = messages.COMMANDS if not _user.is_admin() else messages.ADMIN_COMMANDS
    await update.message.reply_text(msg.get(_user))

#command to set preferences
async def preferences(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user.get(update).set_state(user.State.START)
    await userconfig.progress(update, context)

#command to get information about the lunch bot
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(messages.INFO.get(user.get(update)))

#command to get information about lottery
async def lottery_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not lottery.is_scheduled:
        msg = messages.LOTTERY_ON_PAUSE
    elif lottery.is_active(): 
        msg = messages.lottery_active(lottery.time_until_event())
    else: 
        msg = messages.lottery_not_active(lottery.time_until_event())
    await update.message.reply_text(msg.get(user.get(update)))

#command to join lottery
async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _user = user.get(update)
    if _user.configured & (not _user.joined):
        if lottery.is_active():
            _user.set_joined(True)
            i = 0
        else: i = 3
    elif not _user.configured: i = 1
    elif _user.joined: i = 2
    await update.message.reply_text(messages.JOIN[i].get(_user))

#command to cancel partipication to lottery
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _user = user.get(update)
    if _user.joined:
        _user.set_joined(False)
        i = 0
    else: i = 1
    await update.message.reply_text(messages.CANCEL[i].get(_user))

#command to get list of restaurants
async def restaurants(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _user = user.get(update)
    await update.message.reply_text(messages.RESTAURANTS.get(_user))

#command to get random restaurant
async def spin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    restaurants = ("A", "B", "D", "KV", "SK", "Q", "T", "TF", "TS")
    _user = user.get(update)
    await update.message.reply_text(messages.spin(random.choice(restaurants)).get(_user))

#ADMIN COMMANDS:
#command to schedule monthly lotteries
async def schedule_lottery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _user = user.get(update)
    if _user.is_admin():
        msg = messages.lottery_scheduled()
        if context.args is not None:
            if (len(context.args) == 2):
                days = (int(context.args[0]), int(context.args[1]))
                if lottery.change_days(days):
                    lottery.schedule(True, context.application)
                    if lottery.is_active():
                        await callbacks.lottery_notification(context)
                    msg = messages.lottery_scheduled(days)
        await update.message.reply_text(msg.get(_user))
    else:
        await update.message.reply_text(messages.NOT_COMMAND.get(_user))

#check admin command confirmation
def confirmation(args: "list[str] | None") -> bool:
    if args is not None:
        if (len(args) == 1):
            if (args[0] == "confirm"): return True
    return False

#command to pause monthly lotteries
async def pause_lottery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _user = user.get(update)
    if _user.is_admin():
        if not confirmation(context.args): 
            await update.message.reply_text(messages.PAUSE_LOTTERY_FAILED.get(_user))
        else:
            #check if lottery is currently scheduled
            if lottery.is_scheduled:
                lottery.schedule(False, context.application)
                for u in user.joined_users(): u.set_joined(False, log=False)
                msg = messages.lottery_paused(True)
            else: msg = messages.lottery_paused(False)
            await update.message.reply_text(msg.get(_user))
    else:
        await update.message.reply_text(messages.NOT_COMMAND.get(_user))

#command to start lottery result immediately
async def start_lottery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _user = user.get(update)
    if _user.is_admin():
        if not confirmation(context.args):
            await update.message.reply_text(messages.START_LOTTERY_FAILED.get(_user))
        else:
            await callbacks.lottery_result(context)
    else:
        await update.message.reply_text(messages.NOT_COMMAND.get(_user))

#command to get bot.log
async def get_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _user = user.get(update) 
    if _user.is_admin():
        await update.message.reply_document(filehandler.LOG_FP)
    else:
        await update.message.reply_text(messages.NOT_COMMAND.get(_user))