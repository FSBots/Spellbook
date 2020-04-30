import time
import telepot
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space, include_callback_query_chat_id
from telepot.namedtuple import InlineKeyboardMarkup,ForceReply
from spellbook_db import Spellbook


class Handler(telepot.helper.ChatHandler):

    classKeyboard = None
    levelKeyboard = None
    menuKeyboard = None
    spellbook = None

    class_to_find = None
    level_to_find = None
    level_expected = False

    #Menu buttons
    menu = [['Nome','Livello'],['Classe e Livello']]

    classes = [['Bardo','Chierico','Druido','Mago'],
               ['Paladino','Ranger','Stregone','Warlock']]

    levels = [['Lv. 0','Lv. 1','Lv. 2','Lv. 3','Lv. 4'],
              ['Lv. 5','Lv. 6','Lv. 7','Lv. 8','Lv. 9']]

    short_levels = [['Lv. 1', 'Lv. 2', 'Lv. 3', 'Lv. 4','Lv. 5']]

    #Chat id
    chat_id_boss = [1936841,81503607]

    def __init__(self, *args, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)
        #Spell book initialization
        self._spell_editor = None
        #Message editor initialization
        self._editor = None
        #Forced reply message editor initialization
        self._forcedreply_editor = None

        #Database connection
        self.spellbook = Spellbook("root", "capitanoxxx", "localhost", "dnd_5_incantesimi")

        #Menu initialization
        self.menuKeyboard = InlineKeyboardMarkup(inline_keyboard=self._get_keyboard(self.menu,'menu'))
        self.classKeyboard = InlineKeyboardMarkup(inline_keyboard=self._get_keyboard(self.classes,'class'))
        self.levelKeyboard = InlineKeyboardMarkup(inline_keyboard=self._get_keyboard(self.levels,'level'))
        self.shortlevelKeyboard = InlineKeyboardMarkup(inline_keyboard=self._get_keyboard(self.short_levels,'level'))

    #Callback buttons
    #menu,Nome | menu,Classe | menu,Livello | menu,Classe e Livello
    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        data = str(query_data).split(',')
        if data[0] == 'menu':
            if data[1] == 'Nome':
                markup = ForceReply()
                _forcedreply = bot.sendMessage(self.chat_id,'Spara un nome!', reply_markup=markup)
                self._forcedreply_editor = telepot.helper.Editor(self.bot, _forcedreply)
            elif data[1] == 'Classe':
                self._send_classes()
            elif data[1] == 'Livello':
                self._send_levels()
            elif data[1] == 'Classe e Livello':
                self.level_expected = True
                self._send_classes()
        elif data[0] == 'class':
            self.class_to_find = data[1]
            if self.level_expected:
                self._send_levels()
            else:
                self._send_spells(self.spellbook.get_spells_by_class(self.class_to_find), 2)
        elif data[0] == 'level':
            self.level_to_find = data[1].replace('Lv. ', '')
            if self.level_expected:
                self._send_spells(self.spellbook.get_spells_by_class_level(self.class_to_find, self.level_to_find), 0)
            else:
                self._send_spells(self.spellbook.get_spells_by_level(self.level_to_find), 1)
        elif data[0] == 'spell':
            self._send_spell_message(data[1])

    def on_chat_message(self,msg):
        text = msg['text'].lower()
        if text == '/start' or text == 'start':
            #Delete all
            self._cancel_last()
            #self._cancel_last_spell()
            self._cancel_forced_reply()
            self.level_expected = False
            self.class_to_find = None
            self.level_to_find = None
            #Start with first menu
            if msg['chat']['id'] in self.chat_id_boss:
                self._send_menu('Ciao Babbo miooo!\nRicerca incantesimo per:')
            else:
                self._send_menu()
        else:
            if 'reply_to_message' in msg :
                if msg['reply_to_message']['text'] == 'Spara un nome!':
                    self._send_spells(self.spellbook.get_spells_by_name(text), 3)


    #Timeout expired
    def on__idle(self, event):
        self._cancel_last()
        self._cancel_last_spell()
        self._cancel_forced_reply()
        self.close()


    #Delete of the last message
    def _cancel_last(self):
        if self._editor is not None:
            self._editor.deleteMessage()
            self._editor = None

    #Delete of the last spell message
    def _cancel_last_spell(self):
        if self._spell_editor is not None:
            self._spell_editor.deleteMessage()
            self._spell_editor = None

    #Delete of the last forced reply message
    def _cancel_forced_reply(self):
        if self._forcedreply_editor is not None:
            self._forcedreply_editor.deleteMessage()
            self._forcedreply_editor = None

    #Delete of the last spell and send of the spell passed as parameter
    def _send_spell_message(self,spell):
        for tupla in self.last_spellbook:
            if tupla['Nome'] == spell:
                spell_str = 'Nome: ' + spell + '\n' + \
                        tupla['Tipo'] + ' di livello ' + str(tupla['Livello']) + '\n' + \
                        'Tempo di lancio: ' + tupla['TempoDiLancio'] + '\n' + \
                        'Gittata: ' + tupla['Gittata'] + '\n' + \
                        'Componenti: ' + tupla['Componenti'] + '\n' + \
                        'Durata: ' + tupla['Durata'] + '\n' + \
                        tupla['Descrizione']
                self._cancel_last_spell()
                spell_str = self.restore_windows_1252_characters(spell_str)
                _spell = self.sender.sendMessage(spell_str)
                self._spell_editor = telepot.helper.Editor(self.bot, _spell)

    #Resolution of the errors in message character
    def restore_windows_1252_characters(self,s):
        import re
        def to_windows_1252(match):
            try:
                return bytes([ord(match.group(0))]).decode('windows-1252')
            except UnicodeDecodeError:
                # No character at the corresponding code point: remove it.
                return ''
        return re.sub(r'[\u0080-\u0099]', to_windows_1252, s)

    #Creation of the keyboard for generic spell list
    def _get_keyboard(self, array, callback=''):
        res = list(map(lambda classe: list(map(
            lambda c: dict(text=str(c), callback_data=callback + ',' + str(c)), classe)), array))
        return res

    #Creation of the keyboard before send
    def _get_spell_keyboard(self,spellist,mode):
        #Mode 0 name
        #1 class
        #2 level
        #3 both
        res = []
        for tupla in spellist:
            nome = self.restore_windows_1252_characters(tupla['Nome'])
            if mode == 1:
                classe = tupla['Classe']
                button = dict(text=nome + "[" + classe + "]", callback_data='spell,' + nome)
            elif mode == 2:
                livello = tupla['Livello']
                button = dict(text=nome + " LV " + str(livello), callback_data='spell,' + nome)
            elif mode == 3:
                classe = tupla['Classe']
                livello = tupla['Livello']
                button = dict(text=nome + " LV " + str(livello) + "[" + classe + "]", callback_data='spell,' + nome)
            else:
                button = dict(text=nome, callback_data='spell,' + nome)
            res.append([button])
            if res.__len__() > 70:
                break
        return res


    #MEthod for send message with the inline keyboards

    def _send_spells(self, spellist, mode):
        self._cancel_last()
        self.last_spellbook = spellist
        keyboard = self._get_spell_keyboard(spellist, mode)
        if keyboard.__len__() == 0:
            self.sender.sendMessage('Nessun incantesimo!')
        else:
            spellkeyboard = InlineKeyboardMarkup(inline_keyboard = keyboard)
            sent = self.sender.sendMessage('Incantesimi richiesti:', reply_markup=spellkeyboard)
            self._editor = telepot.helper.Editor(self.bot, sent)

    def _send_classes(self):
        self._cancel_last()
        sent = self.sender.sendMessage('Scegli una classe:', reply_markup=self.classKeyboard)
        self._editor = telepot.helper.Editor(self.bot, sent)

    def _send_levels(self):
        self._cancel_last()

        if self.class_to_find == 'Paladino' or self.class_to_find == 'Ranger':
            sent = self.sender.sendMessage('Scegli il livello:', reply_markup=self.shortlevelKeyboard)
        else:
            sent = self.sender.sendMessage('Scegli il livello:', reply_markup=self.levelKeyboard)
        self._editor = telepot.helper.Editor(self.bot, sent)

    def _send_menu(self,message = 'Ricerca incantesimo per:'):
        self._cancel_last()
        sent = self.sender.sendMessage(message, reply_markup=self.menuKeyboard)
        self._editor = telepot.helper.Editor(self.bot, sent)


#Serious stuff
token = "524296968:AAGPPCJP0PDDLy2RtHvVRN-Ag3V9AYnFG6A"

bot = telepot.DelegatorBot(token, [
    include_callback_query_chat_id(pave_event_space()
                                   )(per_chat_id(types=['private']), create_open, Handler, timeout=3600)
])

MessageLoop(bot).run_as_thread()

print('Listening ...')

while 1:
    time.sleep(10)
