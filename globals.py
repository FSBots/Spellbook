# Globals, no logic file

# Class name selected in a class+level search
LAST_CLASS_NAME = "last_class_name"

# Id of last message sended
# Required for update the spell displayed
LAST_MESSAGE_ID = "last_message_id"

# List of spells requested
CACHED_SPELL = "cached_spell"

# Name of the last spell retrieved
# Required for report function
LAST_SPELL_NAME = "last_spell_name"


# Database object
global spellbook
spellbook = None


def get_spellbook():
    global spellbook
    return spellbook


def set_spellbook(db):
    global spellbook
    spellbook = db


# User list for History(va anche globale?)
global users_list
users_list = ""


def get_users_list():
    global users_list
    return users_list


def set_users_list(name):
    global users_list
    users_list = name
