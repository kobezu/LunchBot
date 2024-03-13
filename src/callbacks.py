import telegram
from telegram.ext import ContextTypes
import messages
import user
from user import users
import logger
from lottery_result import LotteryResult

#send message to user, and if message cannot be sent to the user, remove the user
async def send_message(context: ContextTypes.DEFAULT_TYPE, user_id: int, text: str):
    try:
        await context.bot.send_message(user_id, text)
    except telegram.error.BadRequest as e:
        logger.error(f"BadRequest: " + e.message)
        user.remove(user_id)

#send lunch lottery notification to users
async def lottery_notification(context: ContextTypes.DEFAULT_TYPE):
    msg_sent: list[str] = []
    for _user in users.values():
        if _user.configured:
            await send_message(context, _user.ID, messages.lottery_noti().get(_user))
            msg_sent.append(_user.name)
    logger.info(None, f"\nLottery notification has been sent to users: \n{', '.join(msg_sent)}")

#send lottery reminder to users that aren't joined yet
async def lottery_reminder(context: ContextTypes.DEFAULT_TYPE):
    msg_sent: list[str] = []
    for _user in users.values():
        if _user.configured & (not _user.joined):
            await send_message(context, _user.ID, messages.REMINDER.get(_user))
            msg_sent.append(_user.name)
    logger.info(None, f"\nLottery reminder has been sent to users: \n{', '.join(msg_sent)}")

#send lottery result to users
async def lottery_result(context: ContextTypes.DEFAULT_TYPE):
    #check if any usernames have been changed
    for _user in users.values():
        try:
            u = await context.bot.get_chat(_user.ID)
            new_name = f"@{u.username}"
            if not _user.name == new_name:
                _user.update_name(new_name)
        except telegram.error.BadRequest as e:
            logger.error(f"BadRequest: " + e.message)
            user.remove(_user.ID)

    attendance = len(user.joined_users())
    result = LotteryResult()
    for group in result.groups:
        #groups size of two
        if len(group) == 2:
            for i in range(2):
                await send_message(context, group[i].ID, messages.lottery_result(group[(i+1) % 2]).get(group[i]))
        #groups size of three
        if len(group) == 3:
            for i in range(3):
                await send_message(context, group[i].ID, messages.lottery_result(group[(i+1) % 3], group[(i+2) % 3]).get(group[i]))
        #make users in group not joined again
        for _user in group:
            _user.set_joined(False, log=False)
    #send message to users not in groups and set them not joined
    for _user in result.not_in_group:
        await send_message(context, _user.ID, messages.NO_PARTNER.get(_user))
        _user.set_joined(False, log=False)
        
    def group_str(group: "list[user.User]") -> str:
        return f"[{', '.join(map(lambda u: u.name, group))}]"
    
    logger.info(None, f"""
    Lottery result: 
    {attendance} people joined
    Groups ({len(result.groups)}): {', '.join(map(group_str, result.groups))}
    User(s) not in groups: {group_str(result.not_in_group)}""")

