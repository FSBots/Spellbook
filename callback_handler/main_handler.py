from callback_handler.level_class_handler import callback_level
from callback_handler.spell_handler import callback_name
from callback_handler.spell_options_handler import callback_spell_options, callback_report
from keyboard_manager import *
from message_manager import *


## Main handler
#@param update : message context
#@param context : user context
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
    elif callback == "school":
        context.user_data[LAST_SCHOOL_NAME] = choice
        callback_menu(update, context, "Livello")


## Callback of a main menu click
#@param update : message context
#@param context : user context
#@param choice : button pressed as string
def callback_menu(update, context, choice):
    message = update.callback_query.message

    if choice == "Nome":
        send_forced_message(update.callback_query, context, FORCED_REPLY_MESSAGE)

    elif choice == "Livello":
        keyboard = get_levels_keyboard()
        text = LEVELS_MESSAGE
        edit_message(update.callback_query, context, text, keyboard)

    elif choice == "Classe e livello":
        keyboard = get_classes_keyboard()
        text = CLASSES_MESSAGE
        edit_message(update.callback_query, context, text, keyboard)

    elif choice == "Scuola e livello":
        keyboard = get_schools_keyboard()
        text = SCHOOLS_MESSAGE
        edit_message(update.callback_query, context, text, keyboard)

    elif choice == "Recenti":
        spells = get_spellbook().get_spells_history(message.chat_id, HISTORY_LIMIT)
        keyboard = get_spells_keyboard(spells, "level")
        if spells:
            context.user_data[CACHED_SPELL] = spells
            text = SPELL_MESSAGE
        else:
            text = NO_SPELL_MESSAGE
        edit_message(update.callback_query, context, text, keyboard)

    elif choice == "Statistiche":
        stats = get_spellbook().get_stats(message.chat_id)
        edit_message(update.callback_query, context, get_stats_message(stats))
        keyboard = get_menu_keyboard()
        send_message(update.callback_query, context, STARTING_MESSAGE, keyboard)

##Get DB stats as formatted string
#@param stats : result set of get_stats query as dictionary
#@return stats as formatted string
def get_stats_message(stats):
    return "<b>Statistiche globali:</b>" + \
           "\nUtenti totali: " + str(stats["total_users"]) + \
           "\nUtenti online: " + str(stats["current_online"]) + \
           "\nSpell piú richiesta: " + stats["favourite_spell"] + \
           "\n\n<b>Statistiche personali:</b>" + \
           "\nSpell piú richiesta: " + stats["your_favourite_spell"]


## Callback of a Reply message, used for requests by name
#@param update : message context
#@param context : user context
def reply_message_callback_handler(update, context):
    # Db request
    spells = get_spellbook().get_spells_by_name(update.message.text)
    keyboard = get_spells_keyboard(spells, "classlevel")
    if spells:
        context.user_data[CACHED_SPELL] = spells
        text = SPELL_MESSAGE
    else:
        text = NO_SPELL_MESSAGE
    send_message(update, context, text, keyboard)
