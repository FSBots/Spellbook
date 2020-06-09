import telegram
from telegram import ForceReply


def send_message(update, context, text, keyboard=None):
    return context.bot.send_message(
        chat_id=update.message.chat_id,
        parse_mode=telegram.ParseMode.HTML,
        text=text,
        reply_markup=keyboard
    )


def send_forced_message(update, context, text):
    return context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        reply_markup=ForceReply()
    )


def edit_message_by_id(update, context, message_id, text, keyboard=None):
    return context.bot.edit_message_text(
        chat_id=update.message.chat_id,
        message_id=message_id,
        parse_mode=telegram.ParseMode.HTML,
        text=text,
        reply_markup=keyboard
    )


def edit_message(update, context, text, keyboard=None):
    edit_message_by_id(update, context, update.message.message_id,  text, keyboard)


def delete_message(update, context, message_id):
    return context.bot.delete_message(
        chat_id=update.message.chat_id,
        message_id=message_id
    )