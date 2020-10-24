from telegram.error import NetworkError
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from bot_token import token
from callback_handler.main_handler import main_callback_handler, reply_message_callback_handler
from globals import *
from message_manager import *
from spellbook_db import Spellbook
import random


def initialize_context(context):
    try:
        context.user_data["Name"]
    except:
        context.user_data["Name"] = ""


def reset_context(context):
    context.user_data["IdSpellGroup"] = ""
    context.user_data["Name"] = ""
    context.user_data["Description"] = ""
    context.user_data["NewName"] = ""
    context.user_data["NewDescription"] = ""


def get(update, context):
    initialize_context(context)
    if context.user_data["Name"] == "":
        spell = random.choice((get_spellbook().get_spell_to_modify()))
        context.user_data["IdSpellGroup"] = spell["IdSpellGroup"]
        context.user_data["Name"] = spell["Name"]
        context.user_data["Description"] = spell["Description"]
    message = "Incantesimo da modificare: " + context.user_data["Name"] + "\n\n" + context.user_data["Description"]
    send_message(update, context, message)
    context.user_data["send_description"] = False
    context.user_data["NewName"] = ""
    context.user_data["NewDescription"] = ""


# /set
def set(update, context):
    initialize_context(context)
    if context.user_data["Name"] != "":
        message = "Butta il nuovo nome di " + context.user_data["Name"]
        send_forced_message(update, context, message)
        context.user_data["send_description"] = True
    else:
        send_message(update, context, "Oh, un fare il furbo! Fai /get !")


# /start
def start(update, context):
    initialize_context(context)
    message = "Wee, questi sono i comandi eh, fai per benino! \n" \
              "- /get per ottenere una spell da riarronzare \n" \
              "- /set per inserire una spell riarronzata \n" \
              "Grazie Capitano che porti la pace fra noi"
    send_message(update, context, message)


# /error
def error(update, context):
    logger.warning('Update "%s"', update)
    logger.warning('Error "%s"', context.error)


def reply_function(update, context):
    if context.user_data["send_description"]:
        message = "Butta la nuova descrizione di " + context.user_data["Name"]
        send_forced_message(update, context, message)
        print(update.message.text)
        context.user_data["NewName"] = update.message.text
    else:
        context.user_data["NewDescription"] = update.message.text
        print(update.message.text)
        get_spellbook().insert_new_spell_version(context.user_data["IdSpellGroup"], context.user_data["NewName"], context.user_data["NewDescription"], update.message.chat.username)
        send_message(update, context, "Grazie bro!")
        reset_context(context)

    context.user_data["send_description"] = False


def main():
    logger.info("Everything is started")
    set_spellbook(Spellbook())  # Database initialization
    updater = Updater(token, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('set', set))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(main_callback_handler))
    updater.dispatcher.add_handler(CommandHandler('get', get))
    updater.dispatcher.add_handler(MessageHandler(Filters.reply, reply_function))
    updater.dispatcher.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
