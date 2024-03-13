import user
from user import User, Language
import lottery
import filehandler

#message class that reads message text from file, if file name is given, otherwise from the given text parameter
class Message:
    def __init__(self, file_name: "str | None"=None, text: "tuple[str, str]" =('','')):
        self.FIN = filehandler.message_txt(file_name, True) if file_name is not None else text[0]
        self.ENG = filehandler.message_txt(file_name, False) if file_name is not None else text[1]
    #get message text in user's language
    def get(self, _user: User) -> str:
        if _user.bot_language == Language.FIN: return self.FIN
        else: return self.ENG

#welcome message
WELCOME = Message('config/welcome.txt')

#bot language question
BOT_LANGUAGE = Message('config/bot_language.txt')

#lunch language question and answers
LUNCH_LANGUAGE = (Message('config/lunch_language/0.txt'), Message('config/lunch_language/1.txt'),
                Message('config/lunch_language/2.txt'), Message('config/lunch_language/3.txt'))

#config_failed
CONFIG_FAILED = Message('config/config_failed.txt')

#configured message
CONFIGURED = Message('config/configured.txt')

#reply to non-command message
NOT_COMMAND = Message('not_command.txt')

#commands message
COMMANDS = Message('commands/commands.txt')

#info command message
INFO = Message('commands/info.txt')

#join command messages
JOIN = (Message('commands/join/0.txt'), Message('commands/join/1.txt'),
        Message('commands/join/2.txt'), Message('commands/join/3.txt'))

#cancel command messages
CANCEL = (Message('commands/cancel/0.txt'), Message('commands/cancel/1.txt'))

#reply not valid message
def reply_not_valid(reply: str) -> Message:
    return Message(text=(f'"{reply}" ei kelpaa vastaukseksi.', f'"{reply}" is not valid answer.'))

#lunch lottery notification
def lottery_noti() -> Message: 
    return Message(text=("Lounaslotto on tulossa! Komennolla /tietoa saat lisätietoa ja komennolla /liity osallistut arvontaan. " + 
                   f"Arvonta suoritetaan tämän kuun {lottery.result_day}. päivä. Onnea arvontaan!", 
                    "The lunch lottery is coming! Use the command /info for more information and the command /join to enter the draw. " +
                    f"The draw is held on the {lottery.result_day}. day of this month. Good luck in the draw!"))

#lunch lottery reminder
REMINDER = Message('lottery/reminder.txt')

#failed to found partner message
NO_PARTNER = Message('lottery/no_partner.txt')

#lunch lottery result message
def lottery_result(partner_1: User, partner_2: "User | None" =None) -> Message:
    #check if there is second partner
    if partner_2 is not None:
        return Message(text=(f"Lounaslottoparisi ovat... {partner_1.name} ja {partner_2.name}! " + 
                       "Sopikaa yhdessä teille sopiva aika lounasta varten. Hyvää lounasta ja hedelmällisiä keskusteluja!", 
                       f"Your lunch lottery pairs are... {partner_1.name} and {partner_2.name}! " +
                       "Agree on a lunch time that works for both of you. Enjoy your lunch and have fruitful conversations!"))
    #only one partner
    else:
        return Message(text=(f"Lounaslottoparisi on... {partner_1.name}! " +
                       "Sopikaa yhdessä teille sopiva aika lounasta varten. Hyvää lounasta ja hedelmällisiä keskusteluja!", 
                       f"Your lunch lottery pair is... {partner_1.name}! " +
                       "Agree on a lunch time that suits you all. Enjoy your lunch and have fruitful conversations!"))

#return string containing time until event 
def time_str(time: "tuple[int, int, int]", finnish: bool) -> str:
    def build_str(num: int, word: str, letter: str) -> str:
        if num == 1: return f"{num} {word}"
        else: return f"{num} {word}{letter}"
    if finnish:
        return f"{build_str(time[0], 'päivä', 'ä')}, {build_str(time[1], 'tunti', 'a')} ja {build_str(time[2], 'minuutti', 'a')}"
    else:
        return f"{build_str(time[0], 'day', 's')}, {build_str(time[1], 'hour', 's')} and {build_str(time[2], 'minute', 's')}"

#lottery active message
def lottery_active(time: "tuple[int, int, int]") -> Message:
    count = len(user.joined_users())
    return Message(text=(f"Lounaslotto on aktiivinen. Osallistuneita tällä hetkellä ({count}). Arvontaan on jäljellä {time_str(time, True)}.", 
                    f"Lunch lottery is active. Participants currently ({count}). Time until the draw: {time_str(time, False)}."))

#lottery not active message
def lottery_not_active(time: "tuple[int, int, int]") -> Message:
    return Message(text=(f"Lounaslotto ei ole aktiivinen. Seuraavan alkuun on {time_str(time, True)}.", 
                    f"Lunch lottery is not active. Time until the next one: {time_str(time, False)}."))

LOTTERY_ON_PAUSE = Message('commands/lottery/lottery_on_pause.txt')

#MESSAGES FOR ADMINS
#admin_commands message
ADMIN_COMMANDS = Message('commands/admin/admin_commands.txt')

#lottery scheduled message
def lottery_scheduled(days: "tuple[int, int] | None"=None) -> Message:
    if days is not None: txt = f"Monthly lottery scheduled succesfully. Start day: {days[0]}, and result day: {days[1]}."
    else: txt = ("Lottery scheduling failed. Days must be numbers between 1 and 28, " +
                "and the result day must be greater than the start day. Valid command example: \"/schedule_lottery 1 8\".")
    return Message(text=(txt, txt))

#lottery paused message
def lottery_paused(paused: bool) -> Message:
    txt = "Monthly lunch lottery has now been paused." if paused else "Monthly lunch lottery has already been paused."
    return Message(text=(txt, txt))

#pause lottery failed message
PAUSE_LOTTERY_FAILED = Message('commands/admin/pause_lottery_failed.txt')

#start lottery failed message
START_LOTTERY_FAILED = Message('commands/admin/start_lottery_failed.txt')