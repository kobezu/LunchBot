import telegram
from telegram.ext import Application, MessageHandler, filters
import handlers
import user
import logger
import os

#main program
def main():
    logger.info(None, 'Starting bot...')
    try:
        app = Application.builder().token(open(os.path.join(os.path.dirname(__file__), '..', 'files/token.txt'), "r").readline()).build()
    except FileNotFoundError:
        logger.error("FileNotFoundError: Create 'token.txt' file into the 'files' folder. Write the bot token in the first line.")
    except telegram.error.InvalidToken:
        logger.error("InvalidToken: Write your bot token in the first line of the 'token.txt' file.")

    #add handlers
    app.add_error_handler(handlers.error_handler)
    for cmd_handler in handlers.COMMAND_HANDLERS: app.add_handler(cmd_handler)
    app.add_handler(MessageHandler(filters.TEXT, handlers.message_handler))

    #load users from file
    user.load_users(user.USERS_FP)

    logger.info(None, 'Polling...')
    app.run_polling(poll_interval=2)

if __name__ == '__main__':
    main()