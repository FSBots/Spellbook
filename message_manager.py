import telegram
from telegram import ForceReply

# Globals
global last_message_id
last_message_id = None

global cached_spells
cached_spells = None

global last_class_name
last_class_name = ""


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


# Normal Message
def send_message_text(bot, chat_id, text):
    return bot.send_message(
        chat_id=chat_id,
        text=text
    )


# Forced reply message
def send_forced_message(bot, chat_id, text):
    return bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=ForceReply()
    )


# Message with keyboard
def send_message_with_keyboard(bot, chat_id, text, keyboard):
    return bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboard
    )


def edit_message_with_keyboard(bot, chat_id, message_id, text, keyboard):
    return bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=keyboard
    )


# Html message for image link
def send_html_message(bot, chat_id, text):
    return bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=telegram.ParseMode.HTML
    )


def edit_last_html_message(bot, chat_id, text):
    return edit_html_message(bot, chat_id, get_last_message_id(), text)


def edit_html_message(bot, chat_id, message_id, text):
    return bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        parse_mode=telegram.ParseMode.HTML
    )
