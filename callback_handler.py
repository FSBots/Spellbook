from keyboard_manager import *
from message_manager import *

FORCED_REPLY_MESSAGE = "Spara un nome!"
LEVELS_MESSAGE = "Scegli un livello:"
CLASSES_MESSAGE = "Scegli una classe:"
SPELL_MESSAGE = "Scegli un incantesimo:"
NO_SPELL_MESSAGE = "Nessun incantesimo trovato!"
HISTORY_LIMIT = "5"


# Saving of the users list and check if current chat_id is there
# if not, we insert the user in the db
def initialize_users(chat_id):
    users = get_spellbook().get_users()
    if not users.__contains__(chat_id):
        get_spellbook().add_user(chat_id)
        users.append(chat_id)
    set_users_list(users)


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
    elif callback == "class":
        set_last_class_name(choice)
        callback_menu(update, context, "Livello")


# Callback of a main menu click
def callback_menu(update, context, choice):
    message = update.callback_query.message
    set_last_message_id(None)

    if choice == "Nome":
        send_forced_message(context.bot, message, FORCED_REPLY_MESSAGE)

    elif choice == "Livello":
        keyboard = get_levels_keyboard()
        text = LEVELS_MESSAGE
        edit_message_with_keyboard(context.bot, message, text, keyboard)

    elif choice == "Classe e livello":
        keyboard = get_classes_keyboard()
        text = CLASSES_MESSAGE
        edit_message_with_keyboard(context.bot, message, text, keyboard)

    elif choice == "Recenti":
        spells = get_spellbook().get_spells_history(message.chat_id, HISTORY_LIMIT)
        keyboard = get_spells_keyboard(spells, "classlevel")
        if spells:
            set_cached_spells(spells)
            text = SPELL_MESSAGE
        else:
            text = NO_SPELL_MESSAGE
        edit_message_with_keyboard(context.bot, message, text, keyboard)

    elif choice == "Statistiche":
        send_message_text(context.bot, message, "NO!")


# Callback of a spell request
# Update the last spell retrieved with the new one
def callback_name(update, context, choice):
    bot = context.bot
    message = update.callback_query.message
    spell = get_spell_from_cache(choice)
    if get_last_message_id() is not None:
        edit_last_html_message(bot, message, spell)
    else:
        message_sended = send_html_message(bot, message, spell)
        set_last_message_id(message_sended.message_id)
    get_spellbook().add_in_history_by_id(message.chat_id, choice)


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
    if spells:
        set_cached_spells(spells)
        text = SPELL_MESSAGE
    else:
        text = NO_SPELL_MESSAGE
    edit_message_with_keyboard(bot, message, text, keyboard)


# Callback of a general message
def message_callback_handler(update, context):
    message = update.message
    bot = context.bot
    # Db request
    spells = get_spellbook().get_spells_by_name(message.text)
    set_cached_spells(spells)
    keyboard = get_spells_keyboard(spells, "classlevel")
    if spells:
        set_cached_spells(spells)
        text = SPELL_MESSAGE
    else:
        text = NO_SPELL_MESSAGE
    send_message_with_keyboard(bot, message, text, keyboard)