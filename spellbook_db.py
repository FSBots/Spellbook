import pymysql

from db_credentials import *
from globals import logger

pymysql.install_as_MySQLdb()
import MySQLdb


class Spellbook:
    database_connection = None
    cursor = None

    def __init__(self):
        self.database_connection = MySQLdb.connect(address, username,
                                                   password, db_name)
        self.cursor = self.database_connection.cursor()
        logger.info("Database initialized")

    def check_connection(self):
        try:
            self.cursor.execute("SELECT VERSION()")
            results = self.cursor.fetchone()
            # Check if anything at all is returned
            if results:
                return True
            else:
                logger.error("Error to execute query")
                self.__init__()
                return False
        except MySQLdb.Error:
            logger.error("Error in connection")
            self.__init__()
        return False

    def __del__(self):
        self.database_connection.close()
        self.cursor = None

    def get_spells_by_level(self, lvl):
        query = ("CALL `get_spells_by_level`('" + str(lvl) + "');")
        return self.get_query_result_complete(query)

    def get_spells_by_class_level(self, spell_class, spell_lvl):
        query = ("CALL `get_spells_by_class_level`('" + spell_class + "','" + str(spell_lvl) + "');")
        return self.get_query_result(query)

    def get_spells_by_level_school(self, spell_school, spell_lvl):
        query = ("CALL `get_spells_by_level_school`('" + str(spell_lvl) + "','" + spell_school + "');")
        return self.get_query_result_complete(query)

    def get_spells_by_class(self, spell_class):
        query = ("CALL `get_spells_by_class`('" + spell_class + "');")
        return self.get_query_result(query)

    def get_spells_by_name(self, spell_name):
        query = ("CALL `get_spells_by_name`('" + spell_name + "');")
        return self.get_query_result_complete(query)

    def get_query_result(self, query):
        self.check_connection()
        self.cursor.execute(query)
        content_list = []
        aux = {}
        for row in self.cursor:
            aux["IdSpellGroup"] = row[1]
            aux["Author"] = row[2]
            aux["Version"] = row[3]
            aux["Manual"] = row[4]
            aux["Name"] = row[5]
            aux["School"] = row[6]
            aux["Level"] = row[7]
            aux["CastingTime"] = row[8]
            aux["Range"] = row[9]
            aux["Components"] = row[10]
            aux["Duration"] = row[11]
            aux["Description"] = row[12]

            content_list.append(aux)
            aux = {}
        return content_list

    def get_query_result_complete(self, query):
        self.check_connection()
        self.cursor.execute(query)
        content_list = []
        aux = {}
        for row in self.cursor:
            aux["IdSpellGroup"] = row[1]
            aux["Author"] = row[2]
            aux["Version"] = row[3]
            aux["Manual"] = row[4]
            aux["Name"] = row[5]
            aux["School"] = row[6]
            aux["Level"] = row[7]
            aux["CastingTime"] = row[8]
            aux["Range"] = row[9]
            aux["Components"] = row[10]
            aux["Duration"] = row[11]
            aux["Description"] = row[12]
            aux["Class"] = row[13]

            content_list.append(aux)
            aux = {}
        return content_list

    def add_user(self, user_id):
        self.check_connection()
        try:
            query = ("CALL `add_user`('" + str(user_id) + "');")
            self.cursor.execute(query)
            self.database_connection.commit()
            return True
        except:
            return False

    def add_in_history_by_id(self, user_id, spell_name):
        self.check_connection()
        try:
            query = ("CALL `add_in_history_by_id`('" + str(user_id) + "','" + spell_name + "');")
            self.cursor.execute(query)
            self.database_connection.commit()
            return True
        except:
            return False

    def add_in_reports_by_id(self, user_id, spell_name, report):
        self.check_connection()
        try:
            query = ("CALL `add_in_reports_by_id`('" + str(user_id) + "','" + spell_name + "','" + report + "');")
            self.cursor.execute(query)
            self.database_connection.commit()
            return True
        except:
            return False

    def get_spells_history(self, chat_id, limit):
        query = "CALL get_spells_history('" + str(chat_id) + "','" + str(limit) + "');"
        return self.get_query_result_complete(query)

    def get_stats(self, chat_id):
        self.check_connection()
        query = "CALL get_stats('" + str(chat_id) + "');"
        self.cursor.execute(query)
        stored_results = self.cursor.fetchall()
        content_list = {"total_users": stored_results[0][0], "current_online": stored_results[0][1],
                        "favourite_spell": stored_results[0][2],
                        "your_favourite_spell": stored_results[0][3]}
        return content_list

    def get_spells_history(self, chat_id, limit):
        query = ("CALL get_spells_history('" + str(chat_id) + "','" + str(limit) + "');")
        return self.get_query_result(query)

    def get_users(self):
        self.check_connection()
        query = ("CALL get_user_list();")
        self.cursor.execute(query)
        content_list = []
        for row in self.cursor:
            content_list.append(row[0])
        return content_list

    # Unused methods
    def remove_favourite(self, user_id, spell_name):
        try:
            query = ("CALL `remove_favourite`('" + str(user_id) + "','" + spell_name + "');")
            self.cursor.execute(query)
            self.database_connection.commit()
            return True
        except:
            return False

    def get_favourite(self, user_id):
        query = ("CALL `get_favourite`('" + str(user_id) + "');")
        return self.get_query_result(query)

    def print_result(self, content):
        for tupla in content:
            for nomeColonna, valore in tupla.items():
                print(nomeColonna + " : " + str(valore))
