from telegram.error import BadRequest
from spellbook import logger
from globals import LAST_SPELL_NAME, get_spellbook, CACHED_SPELL, LAST_MESSAGE_ID
from keyboard_manager import get_under_spell_keybord
from message_manager import edit_last_html_message, send_html_message


# Callback of a spell request
# Update the last spell retrieved with the new one
def callback_name(update, context, choice):
    bot = context.bot
    message = update.callback_query.message
    last_message_id = context.user_data[LAST_MESSAGE_ID]
    spell = get_spell_from_cache(context, choice)

    if last_message_id is not None:
        try:
            edit_last_html_message(bot, message, last_message_id, spell, get_under_spell_keybord())
        except BadRequest:
            logger.info("Message is not modified, same spell requested!")
    else:
        message_sended = send_html_message(bot, message, spell, get_under_spell_keybord())
        context.user_data[LAST_MESSAGE_ID] = message_sended.message_id

    context.user_data[LAST_SPELL_NAME] = choice
    get_spellbook().add_in_history_by_id(message.chat_id, choice)


def get_spell_from_cache(context, choice):
    spell = ""
    for tupla in context.user_data[CACHED_SPELL]:
        if tupla['Name'] == choice:
            if tupla['Manual'] == 'Xanathar':
                spell = '<b>' + str.upper(choice) + ' [XAN]\n'
            else:
                spell = '<b>' + str.upper(choice) + '\n'
            spell += tupla['School'] + ' di livello ' + str(tupla['Level']) + '</b>\n' + \
                     '<b>Tempo di lancio: </b>' + tupla['CastingTime'] + '\n' + \
                     '<b>Gittata: </b>' + tupla['Range'] + '\n' + \
                     '<b>Componenti: </b>' + tupla['Components'] + '\n' + \
                     '<b>Durata: </b>' + tupla['Duration'] + '\n' + \
                     '<b>Descrizione: </b>\n' + \
                     tupla['Description']
    return spell
