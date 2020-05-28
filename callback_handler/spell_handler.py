from globals import set_last_spell_name, get_last_message_id, set_last_message_id, get_spellbook, get_cached_spells
from keyboard_manager import get_under_spell_keybord
from message_manager import edit_last_html_message, send_html_message


# Callback of a spell request
# Update the last spell retrieved with the new one
def callback_name(update, context, choice):
    bot = context.bot
    message = update.callback_query.message
    spell = get_spell_from_cache(choice)
    set_last_spell_name(choice)
    if get_last_message_id() is not None:
        edit_last_html_message(bot, message, spell, get_under_spell_keybord())
    else:
        message_sended = send_html_message(bot, message, spell, get_under_spell_keybord())
        set_last_message_id(message_sended.message_id)
    get_spellbook().add_in_history_by_id(message.chat_id, choice)


def get_spell_from_cache(choice):
    spell = ""
    for tupla in get_cached_spells():
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
