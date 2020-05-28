from db_credentials import *
import pymysql

pymysql.install_as_MySQLdb()
import MySQLdb


class Spellbook:
    database_connection = None
    cursor = None

    def __init__(self):
        self.database_connection = MySQLdb.connect(address, username,
                                                   password, db_name)
        self.cursor = self.database_connection.cursor()

    def __del__(self):
        self.database_connection.close()
        self.cursor = None

    def get_spells_by_level(self, lvl):
        query = ("CALL `get_spells_by_level`('"+str(lvl)+"');")
        return self.get_query_result(query)

    def get_spells_by_class_level(self, spell_class, spell_lvl):
        query = ("CALL `get_spells_by_class_level`('"+spell_class+"','"+str(spell_lvl)+"');")
        return self.get_query_result(query)

    def get_spells_by_class(self, spell_class):
        query = ("CALL `get_spells_by_class`('"+spell_class+"');")
        return self.get_query_result(query)

    def get_spells_by_name(self, spell_name):
        query = ("CALL `get_spells_by_name`('"+spell_name+"');")
        return self.get_query_result(query)

    def get_query_result(self, query):
        self.cursor.execute(query)
        content_list = []
        aux = {}
        for row in self.cursor:
            aux["Class"] = row[8]
            aux["Name"] = row[0]
            aux["School"] = row[1]
            aux["Level"] = row[2]
            aux["CastingTime"] = row[3]
            aux["Components"] = row[4]
            aux["Duration"] = row[5]
            aux["Range"] = row[6]
            aux["Description"] = row[7]
            aux["Manual"] = row[9]

            content_list.append(aux)
            aux = {}
        return content_list

    def add_user(self, user_id):
        try:
            query = ("CALL `add_user`('"+str(user_id)+"');")
            self.cursor.execute(query)
            self.database_connection.commit()
            return True
        except:
            return False

    def add_in_history_by_id(self, user_id, spell_name):
        try:
            query = ("CALL `add_in_history_by_id`('"+str(user_id)+"','"+spell_name+"');")
            self.cursor.execute(query)
            self.database_connection.commit()
            return True
        except:
            return False
    
    def add_in_reports_by_id(self, user_id, spell_name, report):
        try:
            query = ("CALL `add_in_reports_by_id`('"+str(user_id)+"','"+spell_name+"','"+report+"');")
            self.cursor.execute(query)
            self.database_connection.commit()
            return True
        except:
            return False

    def get_spells_history(self, chat_id, limit):
        query = "CALL get_spells_history('" + str(chat_id) + "','" + str(limit) + "');"
        return self.get_query_result(query)

    def get_users(self):
        query = "CALL get_users();"
        self.cursor.execute(query)
        content_list = []
        for row in self.cursor:
            content_list.append(row[0])
        return content_list

# Unused methods
    def remove_favourite(self, user_id, spell_name):
        try:
            query = ("CALL `remove_favourite`('"+str(user_id)+"','"+spell_name+"');")
            self.cursor.execute(query)
            self.database_connection.commit()
            return True
        except:
            return False

    def get_favourite(self, user_id):
        query = ("CALL `get_favourite`('"+str(user_id)+"');")
        return self.get_query_result(query)

    def print_result(self, content):
        for tupla in content:
            for nomeColonna, valore in tupla.items():
                print(nomeColonna+" : "+str(valore))
    
    def get_spells_history(self, chat_id, limit):
        query = ("CALL get_spells_history('"+str(chat_id)+"','"+str(limit)+"');")
        return self.get_query_result(query)
    
    def get_users(self):
        query = ("CALL get_users();")
        self.cursor.execute(query)
        content_list = []
        for row in self.cursor:
            content_list.append(row[0])
        return content_list