import user
from user import User, Language
import lottery

#message class
class Message:
    def __init__(self, text_fin: str, text_eng: str):
        self.FIN = text_fin
        self.ENG = text_eng

    #get message text in user's language
    def get(self, _user: User) -> str:
        if _user.bot_language == Language.FIN:
            return self.FIN
        else:
            return self.ENG

#welcome message
def info(welcome: bool) -> Message: 
    txt_fin = ("Hei, olen Ristin Killan Lounasbotti. Järjestän joka kuukausi lounasloton, johon osallistumalla voitat lounasseuraa!\n\n" +
                "Arvontaan voit liittyä mukaan lounasloton ollessa aktiivinen - ilmoitan tästä aina viestillä. " +
                "Liityttyäsi, arvontapäivän tullessa arvon sinulle muista osallistuneista parin, jonka kanssa sovitte keskenään ajan ja paikan yhteiselle lounaalle. " +
                "Näin pääset ehkä tutustumaan toiseen kiltalaiseen paremmin!")
    txt_eng = ("Hello, I'm the Lunchbot of the Guild of Cross. " +
                "Every month, I organize a lunch lottery where, by participating, you'll win a lunch companion!\n\n" +
                "You can participate the draw while the lunch lottery is active - I'll notify you about this via message. " +
                "After you join, when the draw day comes, I'll draw you a pair from other participants, and then together you can arrange a time and place for lunch. " +
                "This way, you might get to know another guild member better!")
    if welcome: msg = Message(txt_fin + "\n\nNyt seuraavaksi kerro vielä mitä kieltä haluat käyttää lounaalla, niin olet sitten valmis liittymään seuraavaan lounaslottoon.", 
                              txt_eng + "\n\nNow, tell me what language you want to use at lunch, and then you'll be ready to join the next lunch lottery.")
    else: msg = Message(txt_fin, txt_eng)
    return msg

#configured message
CONFIGURED = Message("Kaikki on nyt valmista! Kirjoita /komennot, jos halaut listan komennoista.", 
                     "Everything is ready now! Type /commands, if you want a list of commands.")

#reply to non-command message
NOT_COMMAND = Message('Kirjoita /komennot nähdäksesi listan komennoista.', 
                        'Write /commands to see list of commands.')

#help command message
def commands(is_admin: bool) -> Message: 
    list_fin = ('Lista komennoista:\n/mieltymykset - määritä botin ja lounaan kieli\n' +
                '/tietoa - tietoa lounasbotista\n' +
                '/lotto - lounasloton tila\n' +
               '/liity - liity mukaan lounaslottoon\n' +
               '/peru - peru osallistumisesi lounaslottoon')
    list_eng = ('List of commands:\n/preferences - set bot and lunch language\n' +
                '/info - information about the lunch bot\n' +
               '/lottery - status of the lunch lottery\n' +
               '/join - join the lottery\n' +
               '/cancel - cancel your lottery partipication')
    list_admin = ('\n\nAdmin commands:\n/schedule_lottery [start day] [result day] - schedule monthly lottery with given start and result day\n' +
                       '/pause_lottery - pause monthly scheduled lunch lotteries\n' +
                       '/start_lottery - run lunch lottery result immediately')
    msg = Message(list_fin + list_admin, list_eng + list_admin) if is_admin else Message(list_fin, list_eng)
    return msg

#join command message
JOIN: "tuple[Message, Message, Message, Message]" = (Message("Olet nyt mukana arvonnassa!", "You are now part of the draw!"),
                                          Message("Et ole vielä kertonut mieltymyksiäsi. Käytä komentoa /mieltymykset tehdäksesi sen.",
                                                  "You haven't told your preferences yet. Use command /preferences to do so."),
                                          Message("Olet jo mukana arvonnassa.", "You are already part of the draw."),
                                          Message("Lounaslotto ei ole tällä hetkellä aktiivinen.", "Lunch lottery is not currently active."))

#cancel command message                           
CANCEL: "tuple[Message, Message]" = (Message("Olet perunut ilmoittautumisen arvontaan.", "You have canceled your partipication to the draw."),
                                   Message("Et ole ilmoittautunut arvontaan.", "You haven't partipicated in the draw."))

#bot language question
BOT_LANGUAGE = Message("Puhunko minä (botti) suomea vai englantia?", "Do I (bot) speak Finnish or English?")

#lunch language question and answers
LUNCH_LANGUAGE: "tuple[Message, Message, Message, Message]" = (Message("Mitä kieltä haluat puhua lounaalla. Suomea, englantia vai ei väliä?", 
                            "What language you want to speak during lunch. Finnish, English or no preference?"),
                            Message("Selvä, puhut suomea lounaalla.", "Alright, you speak Finnish at the lunch."),
                            Message("Selvä, puhut englantia lounaalla.", "Alright, you speak English at the lunch."),
                            Message("Selvä, puhut suomea tai englantia lounaalla.", "Alright, you speak Finnish or English at the lunch."))

#reply not valid message
def reply_not_valid(reply: str) -> Message:
    return Message(f'"{reply}" ei kelpaa vastaukseksi.', f'"{reply}" is not valid answer.')

#TODO replace short info with /info command
#lunch lottery notification
def lottery_noti() -> Message: 
    return Message("Lounaslotto tulee! Komennolla /tietoa saat lisätietoa ja komennolla /liity osallistut arvontaan. " + 
                   f"Arvonta suoritetaan {lottery.result_day}. päivä tätä kuuta. Onnea arvontaan!", 
                    "The lunch lottery is coming! Use the command /info for more information and the command /join to enter the draw. " + 
                    f"The draw will take place on {lottery.result_day}. day of this month. Good luck in the draw!")

#lunch lottery reminder
REMINDER = Message("*Muistutus* Arvonta on huomenna! Vielä kerkeät mukaan komennolla /liity.", 
                    "*Reminder* The draw is tomorrow! You can still join with the command /join.")

#failed to found partner message
NO_PARTNER = Message("Valitettavasti jäit tällä kertaa ilman lounasseuraa... mutta onneksi uusi arvonta järjestetään pian!", 
                        "Unfortunately you didn't get a lunch partner this time... but fortunately, new draw will be held soon!")

#helper function to return string containing time until event 
def time_str(time: "tuple[int, int, int]", finnish: bool) -> str:
    def build_str(num: int, word: str, letter: str) -> str:
        if num == 1:
            return f"{num} {word}"
        else:
            return f"{num} {word}{letter}"
    if finnish:
        return f"{build_str(time[0], 'päivä', 'ä')}, {build_str(time[1], 'tunti', 'a')} ja {build_str(time[2], 'minuutti', 'a')}"
    else:
        return f"{build_str(time[0], 'day', 's')}, {build_str(time[1], 'hour', 's')} and {build_str(time[2], 'minute', 's')}"

#lottery active message
def lottery_active(time: "tuple[int, int, int]") -> Message:
    return Message(f"Lounaslotto on aktiivinen. Osallistuneita tällä hetkellä ({user.joined_count()}). Arvontaan jäljellä {time_str(time, True)}.", 
                    f"Lunch lottery is active. Participants currently ({user.joined_count()}). Time until draw: {time_str(time, False)}.")

#lottery not active message
def lottery_not_active(time: "tuple[int, int, int]") -> Message:
    return Message(f"Lounaslotto ei ole aktiivinen. Seuraavan alkuun on {time_str(time, True)}.", 
                    f"Lunch lottery is not active. Time until next one: {time_str(time, False)}.")

LOTTERY_ON_PAUSE = Message("Kuukausittaiset lounaslotot ovat tällä hetkellä tauolla. Voit kysyä botin ylläpitäjältä milloin lounaslotto taas käynnistyy.", 
                           "Currently monthly lunch lotteries are on a pause. You can ask from bot admin when the lunch lottery will start again.")

#lunch lottery result message
def lottery_result(partner_1: User, partner_2: User | None =None) -> Message:
    #check if there is second partner
    if isinstance(partner_2, User):
        return Message(f"Lounaslottoparisi ovat... {partner_1.name} ja {partner_2.name}! " + 
                       "Sopikaa yhdessä teille sopiva aika lounasta varten. Hyvää lounasta ja hedelmällisiä keskusteluja!", 
                       f"Your lunch lottery pairs are... {partner_1.name} and {partner_2.name}! " +
                       "Agree on a time that suits both of you for lunch. Enjoy your lunch and fruitful conversations!")
    #only one partner
    else:
        return Message(f"Lounaslottoparisi on... {partner_1.name}! " +
                       "Sopikaa yhdessä teille sopiva aika lounasta varten. Hyvää lounasta ja hedelmällisiä keskusteluja!", 
                       f"Your lunch lottery pair is... {partner_1.name}! " +
                       "Agree on a time that suits both of you for lunch. Enjoy your lunch and fruitful conversations!")

#MESSAGES FOR ADMINS
#lottery scheduled message
def lottery_scheduled(days: "tuple[int, int] | None"=None) -> Message:
    if days is not None: txt = f"Monthly lottery scheduled succesfully. Start day: {days[0]}, and result day: {days[1]}."
    else: txt = ("Lottery scheduling failed. Days must be numbers between 1 and 28, " +
                "and the result day must be greater than the start day. Valid command example: \"/schedule_lottery 1 8\".")
    return Message(txt, txt)

#lottery paused message
def lottery_paused(paused: bool) -> Message:
    txt = "Monthly lunch lottery has now been paused." if paused else "Monthly lunch lottery has already been paused."
    return Message(txt, txt)

PAUSE_LOTTERY_FAILED = Message("Write \"/pause_lottery confirm\" if you are sure that you want to pause monthly scheduled lotteries.",
                            "Write \"/pause_lottery confirm\" if you are sure that you want to pause monthly scheduled lotteries.")

#start lottery failed message
START_LOTTERY_FAILED = Message("Write \"/start_lottery confirm\" if you are sure that you want to run lottery result immediately.",
                            "Write \"/start_lottery confirm\" if you are sure that you want to run lottery result immediately.")