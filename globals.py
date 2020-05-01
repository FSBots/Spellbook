# Globals, no logic class

# Id of last message sended, for update
global last_message_id
last_message_id = None

# Spell list cached
global cached_spells
cached_spells = None

# Needed for class + level search
global last_class_name
last_class_name = ""

# User list for History
global users_list
users_list = ""

# Database object
global spellbook
spellbook = None


def get_spellbook():
    global spellbook
    return spellbook


def set_spellbook(db):
    global spellbook
    spellbook = db


def get_users_list():
    global users_list
    return users_list


def set_users_list(name):
    global users_list
    users_list = name


def get_last_class_name():
    global last_class_name
    return last_class_name


def set_last_class_name(name):
    global last_class_name
    last_class_name = name


def get_cached_spells():
    global cached_spells
    return cached_spells


def set_cached_spells(spells):
    global cached_spells
    cached_spells = spells


def get_last_message_id():
    global last_message_id
    return last_message_id


def set_last_message_id(id):
    global last_message_id
    last_message_id = id