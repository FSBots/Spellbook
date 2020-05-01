from keyboard_manager import *
from message_manager import *

FORCED_REPLY_MESSAGE = "Spara un nome!"
LEVELS_MESSAGE = "Scegli un livello:"
CLASSES_MESSAGE = "Scegli una classe:"
SPELL_MESSAGE = "Scegli un incantesimo:"


# Callback of a general message
def message_callback_handler(update, context):
    message = update.message
    bot = context.bot


# Saving of the users list and check if current chat_id is there
# if not, we insert the user in the db
def initialize_users(chat_id):
    set_users_list(get_spellbook().get_users())
    if not get_users_list().__contains__(chat_id):
        get_spellbook().add_user(chat_id)


# Main handler
def callback_handler(update, context):
    query = update.callback_query
    callback, choice = str(query.data).split(",")

    if callback == "menu":
        callback_menu(update, context, choice)
    elif callback == "name":
        callback_name(update, context, choice)
    elif callback == "level":
        callback_level(update, context, choice)
    elif callback == "classes":
        set_last_class_name(choice)
        callback_menu(update, context, "Livello")


# Callback of a main menu click
def callback_menu(update, context, choice):
    bot = context.bot
    message = update.callback_query.message
    set_last_message_id(None)

    if choice == "Nome":
        send_forced_message(bot, message.chat_id, FORCED_REPLY_MESSAGE)

    elif choice == "Livello":
        keyboard = get_levels_keyboard()
        text = LEVELS_MESSAGE
        edit_message_with_keyboard(bot, message.chat_id, message.message_id, text, keyboard)

    elif choice == "Classe e livello":
        keyboard = get_classes_keyboard()
        text = CLASSES_MESSAGE
        edit_message_with_keyboard(bot, message.chat_id, message.message_id, text, keyboard)

    elif choice == "Recenti":
        send_message_text(bot, message.chat_id, "NO!")

    elif choice == "Statistiche":
        send_message_text(bot, message.chat_id, "NO!")


# Callback of a spell request
# Update the last spell retrieved with the new one
def callback_name(update, context, choice):
    bot = context.bot
    chat_id = update.callback_query.message.chat_id
    spell = get_spell_from_cache(choice)
    if get_last_message_id() is not None:
        edit_last_html_message(bot, chat_id, spell)
    else:
        message_sended = send_html_message(bot, chat_id, spell)
        set_last_message_id(message_sended.message_id)


def get_spell_from_cache(choice):
    spell = ""
    for tupla in get_cached_spells():
        if tupla['Nome'] == choice:
            if tupla['Manuale'] == 'Xanathar':
                spell = '<b>' + str.upper(choice) + ' [XAN]\n'
            else:
                spell = '<b>' + str.upper(choice) + '\n'
            spell += tupla['Tipo'] + ' di livello ' + str(tupla['Livello']) + '</b>\n' + \
                        '<b>Tempo di lancio: </b>' + tupla['TempoDiLancio'] + '\n' + \
                        '<b>Gittata: </b>' + tupla['Gittata'] + '\n' + \
                        '<b>Componenti: </b>' + tupla['Componenti'] + '\n' + \
                        '<b>Durata: </b>' + tupla['Durata'] + '\n' + \
                        '<b>Descrizione: </b>\n' + \
                        tupla['Descrizione']
    return spell


# Callback of level button click (2 cases, only level requests and class + level requests)
def callback_level(update, context, choice):
    bot = context.bot
    message = update.callback_query.message
    # Db request
    spells = []
    keyboards = ""
    if get_last_class_name() != "":
        spells = get_spellbook().get_spells_by_class_level(get_last_class_name(), choice)
        keyboard = get_spells_keyboard(spells, "name")
        set_last_class_name("")
    else:
        spells = get_spellbook().get_spells_by_level(choice)
        keyboard = get_spells_keyboard(spells, "class")
    set_cached_spells(spells)
    edit_message_with_keyboard(bot, message.chat_id, message.message_id, SPELL_MESSAGE, keyboard)


# Callback of a general message
def message_callback_handler(update, context):
    message = update.message
    bot = context.bot
    # Db request
    spells = get_spellbook().get_spells_by_name(message.text)
    set_cached_spells(spells)
    keyboard = get_spells_keyboard(spells, "classlevel")
    send_message_with_keyboard(bot, message.chat_id, SPELL_MESSAGE, keyboard)