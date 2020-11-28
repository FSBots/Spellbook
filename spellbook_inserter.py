from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from bot_token import token
from message_manager import *
from spellbook_db import Spellbook
import random


# Database object
global spellbook
spellbook = None


chat_id_boss = [1936841, 81503607]


def get_spellbook():
    global spellbook
    return spellbook


def set_spellbook(db):
    global spellbook
    spellbook = db


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


def reset_queue_context(context):
    context.user_data["QName"] = ""
    context.user_data["QId"] = ""
    context.user_data["QDescription"] = ""
    context.user_data["QAuthor"] = ""
    context.user_data["QueueId"] = ""
    context.user_data["TrueName"] = ""


def initialize_queue_context(context):
    try:
        context.user_data["QName"]
    except:
        context.user_data["QName"] = ""


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
        message = "Inserisci il nuovo nome di " + context.user_data["Name"]
        send_forced_message(update, context, message)
        context.user_data["send_description"] = True
    else:
        send_message(update, context, "Prima fai /get !")


# /start
def start(update, context):
    initialize_context(context)
    message = "Ciao questi sono i comandi che puoi usare: \n" \
              "- /get per ottenere una spell da riarronzare \n" \
              "- /set per inserire una spell riarronzata \n" \
              "Fai per benino eh! \n\n" \
              "Linee guida: \n" \
              "- Scrivi tutto in prima persona\n" \
              "- Riscrivi il testo a parole tue\n" \
              "- Sintetizza senza ricopiare il testo!\n" \
              "- Modifica qualsiasi riferimento a nomi propri di personaggi e di luoghi (Mordenkainen -> Zio Morde)" \
              "\n\nGrazie a te e famiglia! \nGrazie Capitano G. che portate la pace fra noi! \n\n"

    send_message(update, context, message)


# /check
def check(update, context):
    initialize_queue_context(context)
    chat_id = update.message["chat"]["id"]
    if chat_id in chat_id_boss:
        if context.user_data["QName"] == "":
            spell = get_spellbook().get_spell_from_queue()
            if not spell:
                send_message(update, context, "Votoooo!! Scrivi vai un leggere!")
                return
            context.user_data["TrueName"] = spell["TrueName"]
            context.user_data["QueueId"] = spell["QueueId"]
            context.user_data["QId"] = spell["QId"]
            context.user_data["QName"] = spell["QName"]
            context.user_data["QDescription"] = spell["QDescription"]
            context.user_data["QAuthor"] = spell["QAuthor"]
        message = "Incantesimo da modificare: " + context.user_data["TrueName"] + "\n" + \
                  "Nuovo nome: " + context.user_data["QName"] + "\n\n" + \
                  "Nuova descrizione:\n" + context.user_data["QDescription"]
        send_message(update, context, message)
    else:
        send_message(update, context, "Bah!")


# /accept
def accept(update, context):
    chat_id = update.message["chat"]["id"]
    if chat_id in chat_id_boss:
        if context.user_data["QName"] != "":
            get_spellbook().insert_new_spell_version(context.user_data["QId"], context.user_data["QName"],
                                                        context.user_data["QDescription"], context.user_data["QAuthor"])
            get_spellbook().delete_from_spells_queue(context.user_data["QueueId"])
            reset_queue_context(context)
            send_message(update, context, "Fatto!")
        else:
            send_message(update, context, "Oh, un fare il furbo! Fai /check !")

    else:
        send_message(update, context, "Bah!")


# /delete
def delete(update, context):
    chat_id = update.message["chat"]["id"]
    if chat_id in chat_id_boss:
        if context.user_data["QName"] != "":
            get_spellbook().delete_from_spells_queue(context.user_data["QueueId"])
            reset_queue_context(context)
            send_message(update, context, "Fatto!")
        else:
            send_message(update, context, "Oh, un fare il furbo! Fai /check !")
    else:
        send_message(update, context, "Bah!")


def reply_function(update, context):
    if context.user_data["send_description"]:
        message = "Butta la nuova descrizione di " + context.user_data["Name"]
        send_forced_message(update, context, message)
        print(update.message.text)
        context.user_data["NewName"] = update.message.text
    else:
        context.user_data["NewDescription"] = update.message.text
        print(update.message.text)
        get_spellbook().insert_new_spell_into_queue(context.user_data["IdSpellGroup"], context.user_data["NewName"], context.user_data["NewDescription"], update.message.chat.username)
        send_message(update, context, "L'incantesimo é stato inserito, grazie!")
        reset_context(context)

    context.user_data["send_description"] = False


def main():

    set_spellbook(Spellbook())  # Database initialization
    updater = Updater(token, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('set', set))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('get', get))
    updater.dispatcher.add_handler(CommandHandler('check', check))
    updater.dispatcher.add_handler(CommandHandler('accept', accept))
    updater.dispatcher.add_handler(CommandHandler('delete', delete))
    updater.dispatcher.add_handler(MessageHandler(Filters.reply, reply_function))
    # Start the Bot
    updater.start_polling()
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
