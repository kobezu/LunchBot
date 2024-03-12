import filehandler
filehandler.create_files()

from telegram.error import InvalidToken
from telegram.ext import Application
import handlers
import user
import lottery
import logger

#main program
def main():
    logger.info(None, 'Starting bot...')
    try:
        app = Application.builder().token(open(filehandler.TOKEN_FP, "r").readline()).build()
    except InvalidToken:
        logger.exception("InvalidToken: Write your bot token in the first line of the 'token.txt' file.")

    #add handlers
    app.add_error_handler(handlers.error_handler)
    for handler in handlers.HANDLERS: app.add_handler(handler)

    #load users
    user.load_users()
    #load lottery schedule
    lottery.load_lottery(app)

    logger.info(None, 'Polling...')
    app.run_polling(poll_interval=2)

if __name__ == '__main__':
    main() 