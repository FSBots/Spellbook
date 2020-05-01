import telegram
from telegram import ForceReply
from globals import *

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
