from globals import LAST_SPELL_NAME, get_spellbook, STARTING_MESSAGE
from keyboard_manager import get_menu_keyboard, get_report_keybord
from message_manager import edit_message_with_keyboard, send_html_message


# Callback of a spell option buttons (under a spell)
def callback_spell_options(update, context, choice):
    if choice == "Segnala":
        keyboard = get_report_keybord()
        send_html_message(update.callback_query, context, "Seleziona la parte dell'incantesimo errata:", keyboard)
    elif choice == "Nuova ricerca":
        keyboard = get_menu_keyboard()
        send_html_message(update.callback_query, context, STARTING_MESSAGE, keyboard)


# Callback of a report buttons
def callback_report(update, context, choice):
    bot = context.bot
    message = update.callback_query.message
    spell_to_report = context.user_data[LAST_SPELL_NAME]
    get_spellbook().add_in_reports_by_id(message.chat_id, spell_to_report, choice)
    edit_message_with_keyboard(bot, message, "Segnalazione effettuata!", None)
