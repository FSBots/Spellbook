from globals import *
from keyboard_manager import get_under_spell_keybord
from message_manager import send_message, delete_message, edit_message_by_id


## Callback of a spell request
#@param update : message context
#@param context : user context
#@param choice : button pressed as string ( in this case a spell name )
#@note Updates the last spell retrieved with the new one
#@note Checks if the user has already pressed a button and updates the last message sent
def callback_name(update, context, choice):
    spell = get_spell_from_cache(context, choice)
    parts = splitter(spell)
    last_message_id = context.user_data[LAST_MESSAGE_ID]
    if last_message_id:
        # Spell already requested
        update_messages(context, update, last_message_id, parts)
    else:
        # First spell requested
        send_messages(context, update, parts)
    context.user_data[LAST_SPELL_NAME] = choice
    get_spellbook().add_in_history_by_id(update.callback_query.message.chat_id, choice)

## Change the content of the message with id  = last_message_id
#@param update : message context
#@param context : user context
#@param last_mesage_id : id of a message ( in this case, the last one )
#@param parts : List of string forming the message
#@note if the new message is longer, send the difference as new messages
def update_messages(context, update, last_message_id, parts):
    if len(last_message_id) == len(parts) + 1:  # Same length
        for i in range(len(parts)):
            edit_message_by_id(update.callback_query, context, last_message_id[i], parts[i])

    elif len(last_message_id) < len(parts) + 1:  # New message is longer
        for i in range(len(last_message_id)):
            edit_message_by_id(update.callback_query, context, last_message_id[i], parts[i])
        for i in range(len(last_message_id) + 1, len(parts) + 1):
            message_sended = send_message(update.callback_query, context, parts[i])
            context.user_data[LAST_MESSAGE_ID].append(message_sended.message_id)
        message_sended = send_message(update.callback_query, context, UNDER_SPELL_MESSAGE,
                                      get_under_spell_keybord())
        context.user_data[LAST_MESSAGE_ID].append(message_sended.message_id)

    elif len(last_message_id) > len(parts) + 1:  # New message is smaller
        for i in range(len(parts)):
            edit_message_by_id(update.callback_query, context, last_message_id[i], parts[i])
        edit_message_by_id(update.callback_query, context, last_message_id[len(parts)], UNDER_SPELL_MESSAGE,
                           get_under_spell_keybord())
        for i in range(len(parts) + 1, len(last_message_id)):
            delete_message(update.callback_query, context, last_message_id[i])
            context.user_data[LAST_MESSAGE_ID].remove(last_message_id[i])

## Send message to user
#@param update : message context
#@param context : user context
#@param parts : List of string forming the message to send
def send_messages(context, update, parts):
    for part in parts:
        message_sended = send_message(update.callback_query, context, part)
        context.user_data[LAST_MESSAGE_ID].append(message_sended.message_id)
    message_sended = send_message(update.callback_query, context, UNDER_SPELL_MESSAGE,
                                  get_under_spell_keybord())
    context.user_data[LAST_MESSAGE_ID].append(message_sended.message_id)

## Get the spell from cached ones
#@param context : user context
#@param choice : button pressed as string ( in this case a spell name )
#@return the spell as formatted string
def get_spell_from_cache(context, choice):
    spell = ""
    for tupla in context.user_data[CACHED_SPELL]:
        if tupla['Name'] == choice:
            if tupla['Manual'] == 'Xanathar':
                spell = '<b>' + str.upper(choice) + ' [XAN]\n'
            elif tupla['Manual'] == 'Costa della Spada':
                    spell = '<b>' + str.upper(choice) + ' [CDS]\n'
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

##Split the message in parts to respect MAX_MESSAGE_LENGTH
#@param s : message as string
#@return message as a list of string
def splitter(s):
    parts = []
    while len(s) > 0:
        if len(s) > MAX_MESSAGE_LENGTH:
            i = get_first_space_index(MAX_MESSAGE_LENGTH, s)
            part = s[:i]
            s = s[i + 1:]
        else:
            part = s
            s = ""
        parts.append(part)
    return parts

##Find the index of the first Carriage Return starting from MAX_MESSAGE_LENGTH and going backwards
#@param index : the index where start the resesarch
#@param s : the string where it has to search
#@return the index of the first \n, otherwise return -1
def get_first_space_index(index, s):
    i = index
    while i > 0:
        if s[i] == '\n':
            return i
        else:
            i -= 1
    return index
