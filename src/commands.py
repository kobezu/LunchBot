from telegram import Update
from telegram.ext import ContextTypes
import user
import userconfig
import messages
import lottery
import callbacks

#command to start bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await preferences(update, context)

#command to get list of commands
async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _user = user.get(update)
    await update.message.reply_text(messages.commands(_user.is_admin()).get(_user))

#command to set preferences
async def preferences(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await userconfig.progress(update, context)

#command to get information about the lunch bot
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(messages.info(False).get(user.get(update)))

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
                    job_q = context.application.job_queue
                    #remove old jobs
                    for job in job_q.jobs(): job.schedule_removal()
                    #schedule new jobs
                    job_q.run_monthly(callbacks.lottery_notification, when=lottery.LOTTERY_TIME, day=lottery.start_day)
                    job_q.run_monthly(callbacks.lottery_reminder, when=lottery.LOTTERY_TIME, day=(lottery.result_day-1))
                    job_q.run_monthly(callbacks.lottery_result, when=lottery.LOTTERY_TIME, day=lottery.result_day)
                    lottery.set_scheduled(True)
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
            jobs = context.application.job_queue.jobs()
            jobs_n = len(jobs)
            for job in jobs: job.schedule_removal()
            #check if lottery is currently scheduled
            if jobs_n > 0:
                lottery.set_scheduled(False)
                for u in user.users.values(): u.set_joined(False, log=False)
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