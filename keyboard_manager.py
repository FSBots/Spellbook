from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from globals import *


# Create a keyboard from the array passed as parameter
def create_base_keyboard(keyboard, callback_string=""):
    res = []
    col = []
    for row in keyboard:
        for column in row:
            col.append(InlineKeyboardButton(str(column), callback_data=callback_string + "," + str(column)))
        res.append(col)
        col = []
    return res


def get_classes_keyboard():
    keyboard = create_base_keyboard(classes_keyboard, "class")
    return InlineKeyboardMarkup(keyboard)


def get_schools_keyboard():
    keyboard = create_base_keyboard(schools_keyboard, "school")
    return InlineKeyboardMarkup(keyboard)


def get_menu_keyboard():
    keyboard = create_base_keyboard(menu_keyboard, "menu")
    return InlineKeyboardMarkup(keyboard)


def get_under_spell_keybord():
    keyboard = create_base_keyboard(spell_options_keyboard, "spell_options")
    return InlineKeyboardMarkup(keyboard)


def get_report_keybord():
    keyboard = create_base_keyboard(report_keybord, "report")
    return InlineKeyboardMarkup(keyboard)


# Directly created InlineKeyboardButton instances, customized for levels
def get_levels_keyboard():
    keyboard = []
    col = []
    for row in levels_keyboard:
        for column in row:
            col.append(InlineKeyboardButton(str(column), callback_data="level," + str(column)[4:5]))
        keyboard.append(col)
        col = []
    return InlineKeyboardMarkup(keyboard)


# Directly created InlineKeyboardButton instances, composed by [decorated spell name,(callbackstring,spell name]
# Notice that the spell name in the callback is not the same displayed in the button
def get_spells_keyboard(spell_list, mode):
    spells = []
    for tupla in spell_list:
        name = tupla['Name']
        if mode == "class":
            cl = tupla['Class']
            str_button = name + "[" + cl + "]"
            button = InlineKeyboardButton(str_button, callback_data="name," + name)
        elif mode == "level":
            livello = tupla['Level']
            str_button = "Lv" + str(livello) + "-" + name
            button = InlineKeyboardButton(str_button, callback_data="name," + name)
        elif mode == "classlevel":
            cl = tupla['Class']
            livello = tupla['Level']
            str_button = "Lv" + str(livello) + "-" + name + "[" + cl + "]"
            button = InlineKeyboardButton(str_button, callback_data="name," + name)
        elif mode == "name":
            button = InlineKeyboardButton(name, callback_data="name," + name)
        spells.append([button])
        if spells.__len__() > MAX_NUMBER_SPELL:
            break
    return InlineKeyboardMarkup(spells)
