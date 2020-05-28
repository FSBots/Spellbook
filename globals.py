# Globals, no logic file

# Database object
global spellbook
spellbook = None


def get_spellbook():
    global spellbook
    return spellbook


def set_spellbook(db):
    global spellbook
    spellbook = db


# User list for History
global users_list
users_list = ""


def get_users_list():
    global users_list
    return users_list


def set_users_list(name):
    global users_list
    users_list = name


# Needed for class + level search
global last_class_name
last_class_name = ""


def get_last_class_name():
    global last_class_name
    return last_class_name


def set_last_class_name(name):
    global last_class_name
    last_class_name = name


# Id of last message sended
# Required for update the spell displayed
global last_message_id
last_message_id = None


def get_last_message_id():
    global last_message_id
    return last_message_id


def set_last_message_id(id):
    global last_message_id
    last_message_id = id


# Spell list cached
global cached_spells
cached_spells = None


def get_cached_spells():
    global cached_spells
    return cached_spells


def set_cached_spells(spells):
    global cached_spells
    cached_spells = spells


# Name of the last spell retrieved
# Required for report function
global last_spell_name
last_spell_name = None


def get_last_spell_name():
    global last_spell_name
    return last_spell_name


def set_last_spell_name(name):
    global last_spell_name
    last_spell_name = name