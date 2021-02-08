import pymysql

from db_credentials import *
from globals import logger

pymysql.install_as_MySQLdb()
import MySQLdb

## Interface to spellbook DB
class Spellbook:
    database_connection = None
    cursor = None

    ##Constructor, open db connection
    #@param self : self pointer
    def __init__(self):
        self.database_connection = MySQLdb.connect(address, username,
                                                   password, db_name)
        self.cursor = self.database_connection.cursor()
        logger.info("Database initialized")

    ##Check if connection is expired and launch __init__ again
    #@param self : self pointer
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

    ##Destructor, close db connection
    #@param self : self pointer
    def __del__(self):
        self.database_connection.close()
        self.cursor = None

    ##Call get_spells_by_level procedure
    #@param self : self pointer
    #@param lvl : spell level
    #@return Query result set
    #@note lvl is between 0 to 9 [0:9]
    def get_spells_by_level(self, lvl):
        query = ("CALL `get_spells_by_level`('" + str(lvl) + "');")
        return self.get_query_result_complete(query)

    ##Call get_spells_by_class_level procedure
    #@param self : self pointer
    #@param spell_cast : character class ( Bard, Druid ecc.)
    #@param lvl : spell level
    #@return Query result set
    def get_spells_by_class_level(self, spell_class, spell_lvl):
        query = ("CALL `get_spells_by_class_level`('" + spell_class + "','" + str(spell_lvl) + "');")
        return self.get_query_result(query)

    ##Call get_spells_by_level_school procedure
    #@param self : self pointer
    #@param spell_school : spell school
    #@param lvl : spell level
    #@return Query result set
    def get_spells_by_level_school(self, spell_school, spell_lvl):
        query = ("CALL `get_spells_by_level_school`('" + str(spell_lvl) + "','" + spell_school + "');")
        return self.get_query_result_complete(query)

    ##Call get_spells_by_class procedure
    #@param self : self pointer
    #@param spell_cast : character class ( Bard, Druid ecc.)
    #@return Query result set
    def get_spells_by_class(self, spell_class):
        query = ("CALL `get_spells_by_class`('" + spell_class + "');")
        return self.get_query_result(query)

    ##Call get_spells_by_name procedure
    #@param self : self pointer
    #@param spell_name : the spell name, or part of it
    #@return Query result set
    def get_spells_by_name(self, spell_name):
        query = ("CALL `get_spells_by_name`('" + spell_name + "');")
        return self.get_query_result_complete(query)

    ##Create an array of dictionary contating the result set of the query passed as parameter
    #@param self : self pointer
    #@param query : the result set of a query ugo
    #@return Return the result set as an array of dictionary
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

    ##Create an array of dictionary contating the result set of the query passed as parameter
    #differently from get_query_result, implements more columns
    #@param self : self pointer
    #@param query : the result set of a query
    #@return Return the result set as an array of dictionary
    #@see get_query_result
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

    ##Call add_user procedure
    #add new user to the database
    #@param self : self pointer
    #@param user_id : user chat_id
    #@return bool
    def add_user(self, user_id):
        self.check_connection()
        try:
            query = ("CALL `add_user`('" + str(user_id) + "');")
            self.cursor.execute(query)
            self.database_connection.commit()
            return True
        except:
            return False

    ## call add_user procedure
    #add new user to the database
    #@param self : self pointer
    #@param user_id : user chat_id
    #@return bool
    def add_in_history_by_id(self, user_id, spell_name):
        self.check_connection()
        try:
            query = ("CALL `add_in_history_by_id`('" + str(user_id) + "','" + spell_name + "');")
            self.cursor.execute(query)
            self.database_connection.commit()
            return True
        except:
            return False

    ##Call add_in_reports_by_id procedure
    #@param self : self pointer
    #@param user_id : user chat_id
    #@param spell_name : spell name
    #@param report : report type
    #@return bool
    def add_in_reports_by_id(self, user_id, spell_name, report):
        self.check_connection()
        try:
            query = ("CALL `add_in_reports_by_id`('" + str(user_id) + "','" + spell_name + "','" + report + "');")
            self.cursor.execute(query)
            self.database_connection.commit()
            return True
        except:
            return False

    ##Call get_spells_history procedure
    #@param self : self pointer
    #@param chat_id : user chat_id
    #@param limit : result set rows limit
    #@return Query result set
    def get_spells_history(self, chat_id, limit):
        query = "CALL get_spells_history('" + str(chat_id) + "','" + str(limit) + "');"
        return self.get_query_result_complete(query)

    ##Call get_stats procedure
    #@param self : self pointer
    #@param chat_id : user chat_id
    #@return Query result set
    def get_stats(self, chat_id):
        self.check_connection()
        query = "CALL get_stats('" + str(chat_id) + "');"
        self.cursor.execute(query)
        stored_results = self.cursor.fetchall()
        content_list = {"total_users": stored_results[0][0], "current_online": stored_results[0][1],
                        "favourite_spell": stored_results[0][2],
                        "your_favourite_spell": stored_results[0][3]}
        return content_list

    ##Call get_spells_history procedure
    #@param self : self pointer
    #@param chat_id : user chat_id
    #@param limit : result set rows limit
    #@return Query result set
    def get_spells_history(self, chat_id, limit):
        query = ("CALL get_spells_history('" + str(chat_id) + "','" + str(limit) + "');")
        return self.get_query_result(query)

    ##Call get_users procedure
    #@param self : self pointer
    #@return Query result set
    def get_users(self):
        self.check_connection()
        query = ("CALL get_user_list();")
        self.cursor.execute(query)
        content_list = []
        for row in self.cursor:
            content_list.append(row[0])
        return content_list

    ##Unused methods
    def remove_favourite(self, user_id, spell_name):
        try:
            query = ("CALL `remove_favourite`('" + str(user_id) + "','" + spell_name + "');")
            self.cursor.execute(query)
            self.database_connection.commit()
            return True
        except:
            return False

    ##Unused methods
    def get_favourite(self, user_id):
        query = ("CALL `get_favourite`('" + str(user_id) + "');")
        return self.get_query_result(query)

    ##Unused methods
    def print_result(self, content):
        for tupla in content:
            for nomeColonna, valore in tupla.items():
                print(nomeColonna + " : " + str(valore))
