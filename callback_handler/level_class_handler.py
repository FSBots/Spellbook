from globals import *
from keyboard_manager import get_spells_keyboard
from message_manager import edit_message


# Callback of level button click (2 cases, only level requests and class + level requests)
def callback_level(update, context, choice):

    if context.user_data[LAST_CLASS_NAME] != "": # Class-Level
        spells = get_spellbook().get_spells_by_class_level(context.user_data[LAST_CLASS_NAME], choice)
        keyboard = get_spells_keyboard(spells, "name")
        context.user_data[LAST_CLASS_NAME] = ""

    elif context.user_data[LAST_SCHOOL_NAME] != "": # School-Level
        spells = get_spellbook().get_spells_by_level_school(context.user_data[LAST_SCHOOL_NAME], choice)
        keyboard = get_spells_keyboard(spells, "name")
        context.user_data[LAST_SCHOOL_NAME] = ""

    else: # Only Level
        spells = get_spellbook().get_spells_by_level(choice)
        keyboard = get_spells_keyboard(spells, "class")

    if spells:
        context.user_data[CACHED_SPELL] = spells
        text = SPELL_MESSAGE
    else:
        text = NO_SPELL_MESSAGE
    edit_message(update.callback_query, context, text, keyboard)
