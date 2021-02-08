from globals import LAST_SPELL_NAME, get_spellbook, STARTING_MESSAGE, LAST_MESSAGE_ID, REPORT_DONE_MESSAGE, REPORT_MESSAGE
from keyboard_manager import get_menu_keyboard, get_report_keybord
from message_manager import send_message, edit_message


## Callback of a spell option buttons (under a spell)
#@param update : message context
#@param context : user context
#@param choice : button pressed as string
def callback_spell_options(update, context, choice):
    if choice == "Segnala incantesimo":
        keyboard = get_report_keybord()
        send_message(update.callback_query, context, REPORT_MESSAGE, keyboard)
    elif choice == "Nuova ricerca":
        keyboard = get_menu_keyboard()
        send_message(update.callback_query, context, STARTING_MESSAGE, keyboard)
    context.user_data[LAST_MESSAGE_ID] = []


## Callback of a report buttons
#@param update : message context
#@param context : user context
#@param choice : button pressed as string
def callback_report(update, context, choice):
    chat_id = update.callback_query.message.chat_id
    spell_to_report = context.user_data[LAST_SPELL_NAME]
    get_spellbook().add_in_reports_by_id(chat_id, spell_to_report, choice)
    edit_message(update.callback_query, context, REPORT_DONE_MESSAGE, None)

