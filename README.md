**Description**
-   

This is a Telegram bot that orginizes lunch lotteries.
Users are accepted into the bot by the bot admin (random Telegram users are not wanted to use the bot).
After an user is accepted they get to choose the bot's language and the language they want to speak at the lunch. 
The language choice affects to who bot pairs an user with.
Users join into a lunch lottery while it is active (users get notified when lunch a lottery activates). 
When a lunch lottery closes the bot forms random pairs from the participants and notifies each of them. 

**Instructions**
-   

**Get the bot running**
1. Make a new bot in Telegram 
2. Create a token.txt file to the files folder, and add your bot's token into the first line
3. Create a admins.txt file to the files folder, and add your Telegram user into the first line
4. Run main.py
   
**Communicate with the bot**\
After the bot is set running users communicate with it by using commands


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
