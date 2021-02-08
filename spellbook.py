from telegram.error import NetworkError
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from bot_token import token
from callback_handler.main_handler import main_callback_handler, reply_message_callback_handler
from globals import *
from keyboard_manager import get_menu_keyboard
from message_manager import *
from spellbook_db import Spellbook

## chat_id of Frusco and Salo
chat_id_boss = [1936841, 81503607]
## chat_id of an unknown hero
chat_id_dito_lesto = [116842868]


##Generate personalized message based on chat_id
#@param id : user chat_id
#@return starting message as string 
def generate_starting_message(id):
    message = ""
    if id == chat_id_boss[0]:
        message = "Ciao Babbo Salo!\n"
    elif id == chat_id_boss[1]:
        message = "Ciao Babbo Frusco!\n"
    elif id in chat_id_dito_lesto:
        message = "Ciao Dito Lesto!\n"
    return message + STARTING_MESSAGE


## Initialization of the user_data context for storing data
#@param context : served user context
def initialize_context(context):
    context.user_data[LAST_CLASS_NAME] = ""
    context.user_data[LAST_SCHOOL_NAME] = ""
    context.user_data[LAST_MESSAGE_ID] = []
    context.user_data[CACHED_SPELL] = []
    context.user_data[LAST_SPELL_NAME] = ""


## Saved the users list and checked if current chat_id is there, if not, user is inserted the db
# @param chat_id : user chat_id
def initialize_users_list(chat_id):
    users = get_spellbook().get_users()
    if not users.__contains__(chat_id):
        get_spellbook().add_user(chat_id)
        users.append(chat_id)
    set_users_list(users)  # Global user list updated


# Bot Commands

## Implements /start command
# @param update : <Clockers insert here roba>
# @param context : served user context
# @note Network Error exception is raised when bot is unused for some time and then /start is called
def start(update, context):
    keyboard = get_menu_keyboard()
    message = generate_starting_message(update.message["chat"]["id"])
    while True:
        try:
            send_message(update, context, message, keyboard)
        except NetworkError:
            # Network Error exception is raised when bot is unused for some time and then /start is called
            logger.error("Network error, bot unused for some time!")
        else:
            break
    initialize_context(context)
    initialize_users_list(update.message.chat_id)


## Not implemented
def change_language(update, context):
    send_message(update, context, "NO!")


## Implements /help command
# @param update : <Clockers insert here roba>
# @param context : served user context
def help(update, context):
    send_message(update, context, HELP_MESSAGE)

## Implements /credits command
# @param update : <Clockers insert here roba>
# @param context : served user context
def credits(update, context):
    send_message(update, context, CREDITS_MESSAGE)


## Implements /error command
# @param update : <Clockers insert here roba>
# @param context : served user context
def error(update, context):
    logger.warning('Update "%s"', update)
    logger.warning('Error "%s"', context.error)

## main
def main():
    logger.info("Everything is started")
    set_spellbook(Spellbook())  # Database initialization
    updater = Updater(token, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('language', change_language))
    updater.dispatcher.add_handler(CallbackQueryHandler(main_callback_handler))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('credits', credits))
    updater.dispatcher.add_handler(MessageHandler(Filters.reply, reply_message_callback_handler))
    updater.dispatcher.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
