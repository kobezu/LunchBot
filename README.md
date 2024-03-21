**Description**
-   

This is a Telegram bot that orginizes lunch lotteries.
A monthly schedule for the lunch lotteries is set by the bot admin. When a monthly lunch lottery activates, users can join into it, and when it closes, the bot forms random pairs from the participants, taking in account users' languages. Users are accepted into the bot by the bot admin, because random Telegram users are not wanted to use the bot.
After user is accepted into the bot they get to choose the bot's language and the language they want to speak at the lunch. The language choices are Finnish or English.

**Instructions**
-   

**To get the bot running:**
1. Make a new bot in Telegram 
2. Create a token.txt file in the files folder, and add your bot's token to the first line
3. Create a admins.txt file in the files folder, and add your Telegram user id to the first line
4. Run main.py
   
**To communicate with the bot:**\
After the bot is set running, users communicate with it by using commands. 


>**List of user commands:**\
/preferences - allows user to set bot and lunch language\
/info - tells user information about the lunch bot\
/lottery - tells user the status of the lunch lottery and time until it starts/ends\
/join - allows user to join the lunch lottery\
/cancel - allows user to cancel their lottery partipication 

>**List of admin commands:**\
/schedule_lottery [start] [result] - bot schedules monthly lottery with given start and result day\
/pause_lottery - bot pauses monthly scheduled lunch lotteries\
/start_lottery - bot runs lunch lottery results immediately\
/get_log - bot sends message with bot.log file as attachment to the admin