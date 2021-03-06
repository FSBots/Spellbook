# Globals, no logic file

## Class name selected in a class+level search
LAST_CLASS_NAME = "last_class_name"

## Class name selected in a class+level search
LAST_SCHOOL_NAME = "last_school_name"

## Id of last message sended
#@note Required for update the spell displayed
LAST_MESSAGE_ID = "last_message_id"

## List of spells requested
CACHED_SPELL = "cached_spell"

## Name of the last spell retrieved
# Required for report function
LAST_SPELL_NAME = "last_spell_name"

## Number of spells in history
HISTORY_LIMIT = "5"

## Max length of a message (default of telegram API)
MAX_MESSAGE_LENGTH = 4096

## Max number of spells in a single request
# (telegram max buttons in a single message is 100)
MAX_NUMBER_SPELL = 70

import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

## Database object
global spellbook
spellbook = None


def get_spellbook():
    global spellbook
    return spellbook


def set_spellbook(db):
    global spellbook
    spellbook = db


## User list for History
global users_list
users_list = ""


def get_users_list():
    global users_list
    return users_list


def set_users_list(name):
    global users_list
    users_list = name


## Button array classes
classes_keyboard = [["Bardo", "Chierico", "Druido", "Mago"],
                    ["Paladino", "Ranger", "Stregone", "Warlock"]]
## Button array schools
schools_keyboard = [["Abiurazione", "Divinazione", "Necromanzia"],
                    ["Invocazione", "Evocazione", "Illusione"],
                    ["Ammaliamento", "Trasmutazione"]]
## Button array levels
levels_keyboard = [["Lv. 0", "Lv. 1", "Lv. 2", "Lv. 3", "Lv. 4"],
                   ["Lv. 5", "Lv. 6", "Lv. 7", "Lv. 8", "Lv. 9"]]
## Button array menu
menu_keyboard = [["Nome", "Livello"], ["Classe e livello"], ["Scuola e livello"], ["Recenti", "Statistiche"]]
## Button array options
spell_options_keyboard = [["Segnala incantesimo", "Nuova ricerca"]]
## Button array report
report_keybord = [["Errore di battitura"], ["Incongruenza con il manuale"]
    , ["Associato a classe errata"], ["Associato a livello errato"]]

# Strings
STARTING_MESSAGE = "Ricerca incantesimo per:"
HELP_MESSAGE = "Aiutati che dio ti aiuta 🙌"

CREDITS_MESSAGE = "Si ringraziano: \n" \
                  "• Capitan Gaetano per il supporto morale e <a href='https://thepigeon.org/'>fisico</a> fornito.\n" \
                  "• Sig.Berti, Sig.Gonfia, Sig.Mesti, Sig.Vaghe per il beta testing.\n" \
                  "• Il gruppo @DungeonsAndDragonsITA per la diffusione del Bot."

SPELL_MESSAGE = "Scegli un incantesimo:"
NO_SPELL_MESSAGE = "Nessun incantesimo trovato!"
FORCED_REPLY_MESSAGE = "Spara un nome!"
LEVELS_MESSAGE = "Scegli un livello:"
CLASSES_MESSAGE = "Scegli una classe:"
SCHOOLS_MESSAGE = "Scegli una scuola:"
UNDER_SPELL_MESSAGE = "Cosa vuoi fare adesso?"
REPORT_DONE_MESSAGE = "Segnalazione effettuata!"
REPORT_MESSAGE = "Seleziona la parte dell'incantesimo errata:"


