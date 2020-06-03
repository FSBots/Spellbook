from callback_handler.level_class_handler import callback_level
from callback_handler.spell_handler import callback_name
from callback_handler.spell_options_handler import callback_spell_options, callback_report
from keyboard_manager import *
from message_manager import *

FORCED_REPLY_MESSAGE = "Spara un nome!"
LEVELS_MESSAGE = "Scegli un livello:"
CLASSES_MESSAGE = "Scegli una classe:"
SPELL_MESSAGE = "Scegli un incantesimo:"
NO_SPELL_MESSAGE = "Nessun incantesimo trovato!"
HISTORY_LIMIT = "5"


# Main handler
def main_callback_handler(update, context):
    query = update.callback_query
    callback, choice = str(query.data).split(",")

    if callback == "menu":
        callback_menu(update, context, choice)
    elif callback == "name":
        callback_name(update, context, choice)
    elif callback == "level":
        callback_level(update, context, choice)
    elif callback == "spell_options":
        callback_spell_options(update, context, choice)
    elif callback == "report":
        callback_report(update, context, choice)
    elif callback == "class":
        context.user_data[LAST_CLASS_NAME] = choice
        callback_menu(update, context, "Livello")


# Callback of a main menu click
def callback_menu(update, context, choice):
    message = update.callback_query.message
    context.user_data[LAST_MESSAGE_ID] = None

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
            context.user_data[CACHED_SPELL] = spells
            text = SPELL_MESSAGE
        else:
            text = NO_SPELL_MESSAGE
        edit_message_with_keyboard(context.bot, message, text, keyboard)

    elif choice == "Statistiche":
        send_message_text(context.bot, message.chat_id, "NO!")


# Callback of a Reply message, used for requests by name
def reply_message_callback_handler(update, context):
    message = update.message
    bot = context.bot
    # Db request
    spells = get_spellbook().get_spells_by_name(message.text)
    keyboard = get_spells_keyboard(spells, "classlevel")
    if spells:
        context.user_data[CACHED_SPELL] = spells
        text = SPELL_MESSAGE
    else:
        text = NO_SPELL_MESSAGE
    send_message_with_keyboard(bot, message, text, keyboard)