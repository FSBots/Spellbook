from globals import *
from keyboard_manager import get_spells_keyboard
from message_manager import edit_message_with_keyboard


# Callback of level button click (2 cases, only level requests and class + level requests)
def callback_level(update, context, choice):
    bot = context.bot
    message = update.callback_query.message
    # Db request
    spells = []
    keyboards = ""
    if context.user_data[LAST_CLASS_NAME] != "":
        spells = get_spellbook().get_spells_by_class_level(context.user_data["last_class_name"], choice)
        keyboard = get_spells_keyboard(spells, "name")
        context.user_data[LAST_CLASS_NAME] = ""
    else:
        spells = get_spellbook().get_spells_by_level(choice)
        keyboard = get_spells_keyboard(spells, "class")
    if spells:
        context.user_data[CACHED_SPELL] = spells
        text = SPELL_MESSAGE
    else:
        text = NO_SPELL_MESSAGE
    edit_message_with_keyboard(bot, message, text, keyboard)
