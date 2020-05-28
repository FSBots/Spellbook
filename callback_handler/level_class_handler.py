# Callback of level button click (2 cases, only level requests and class + level requests)
from globals import get_last_class_name, get_spellbook, set_last_class_name, set_cached_spells
from keyboard_manager import get_spells_keyboard
from message_manager import edit_message_with_keyboard



SPELL_MESSAGE = "Scegli un incantesimo:"
NO_SPELL_MESSAGE = "Nessun incantesimo trovato!"

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