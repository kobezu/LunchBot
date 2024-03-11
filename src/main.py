import telegram
from telegram.ext import Application, MessageHandler, filters
import handlers
import user
import lottery
import logger
import filehandler

#main program
def main():
    filehandler.create_files()
    logger.info(None, 'Starting bot...')
    try:
        app = Application.builder().token(open(filehandler.TOKEN_FP, "r").readline()).build()
    except telegram.error.InvalidToken:
        logger.error("InvalidToken: Write your bot token in the first line of the 'token.txt' file.")

    #add handlers
    app.add_error_handler(handlers.error_handler)
    for command_handler in handlers.COMMAND_HANDLERS: app.add_handler(command_handler)
    app.add_handler(MessageHandler(filters.TEXT, handlers.message_handler))

    #load users
    user.load_users()
    #load lottery schedule
    lottery.load_lottery(app)

    logger.info(None, 'Polling...')
    app.run_polling(poll_interval=2)

if __name__ == '__main__':
    main()