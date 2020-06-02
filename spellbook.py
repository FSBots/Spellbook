import logging
from telegram.error import NetworkError
from bot_token import token
from callback_handler.main_handler import *
from message_manager import *
from keyboard_manager import get_menu_keyboard
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from spellbook_db import Spellbook

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Chat id
chat_id_boss = [1936841, 81503607]

# Constants
STARTING_MESSAGE = "Ricerca incantesimo per:"


def generate_starting_message(id):
    message = ""
    if id == chat_id_boss[0]:
        message = "Ciao Babbo Salo!\n"
    if id == chat_id_boss[1]:
        message = "Ciao Babbo Frusco!\n"
    return message + STARTING_MESSAGE


# /start
def start(update, context):
    keyboard = get_menu_keyboard()
    message = generate_starting_message(update.message["chat"]["id"])
    initialize_users_list(update.message.chat_id)
    while True:
        try:
            send_message_with_keyboard(context.bot, update.message, message, keyboard)
        except NetworkError:
            logger.error("NetworkError")
        else:
            break



# Saving the users list and check if current chat_id is there
# if not, we insert the user in the db
def initialize_users_list(chat_id):
    # Recents initialization
    users = get_spellbook().get_users()
    if not users.__contains__(chat_id):
        get_spellbook().add_user(chat_id)
        users.append(chat_id)
    set_users_list(users)


def initialize_db():
    set_spellbook(Spellbook())


# /help
def help(update, context):
    send_message_text(context.bot, update.message, "Use /start to search your D&D Spell!")


# /error
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    initialize_db()
    updater = Updater(token, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(main_callback_handler))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(MessageHandler(Filters.reply, reply_message_callback_handler))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
