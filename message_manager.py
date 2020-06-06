import telegram
from telegram import ForceReply


# Normal Message
def send_html_message(update, context, text, keyboard=None):
    return send_html_message_by_chat_id(context, update.message.chat_id, text, keyboard)


def send_html_message_by_chat_id(context, chat_id, text, keyboard):
    return context.bot.send_message(
        chat_id=chat_id,
        parse_mode=telegram.ParseMode.HTML,
        text=text,
        reply_markup=keyboard
    )











# Forced reply message
def send_forced_message(bot, message, text):
    return bot.send_message(
        chat_id=message.chat_id,
        text=text,
        reply_markup=ForceReply()
    )


def edit_message_with_keyboard(bot, message, text, keyboard):
    return bot.edit_message_text(
        chat_id=message.chat_id,
        message_id=message.message_id,
        text=text,
        reply_markup=keyboard
    )


def edit_last_html_message(bot, message, last_message_id, text, keyboard):
    return bot.edit_message_text(
        chat_id=message.chat_id,
        message_id=last_message_id,
        text=text,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=keyboard
    )


def edit_html_message(bot, message, text):
    return bot.edit_message_text(
        chat_id=message.chat_id,
        message_id=message.message_id,
        text=text,
        parse_mode=telegram.ParseMode.HTML
    )
