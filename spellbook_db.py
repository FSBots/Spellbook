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
        query = ("CALL `ottieniIncantesimiDiLivello`('"+str(lvl)+"');")
        return self.get_query_result(query)

    def get_spells_by_class_level(self, classe, lvl):
        query = ("CALL `ottieniIncantesimiPerClasseDiLivello`('"+classe+"','"+str(lvl)+"');")
        return self.get_query_result(query)

    def get_spells_by_class(self, classe):
        query = ("CALL `ottieniIncantesimiPerClasse`('"+classe+"');")
        return self.get_query_result(query)

    def get_spells_by_name(self, nome):
        query = ("CALL `ottieniIncantesimiPerNome`('"+nome+"');")
        return self.get_query_result(query)

    def get_query_result(self, query):
        self.cursor.execute(query)
        content_list = []
        aux = {}
        for row in self.cursor:
            aux["Classe"] = row[8]
            aux["Nome"] = row[0]
            aux["Tipo"] = row[1]
            aux["Livello"] = row[2]
            aux["TempoDiLancio"] = row[3]
            aux["Componenti"] = row[4]
            aux["Durata"] = row[5]
            aux["Gittata"] = row[6]
            aux["Descrizione"] = row[7]
            aux["Manuale"] = row[9]

            content_list.append(aux)
            aux = {}
        return content_list

#Unused functions
    def add_user(self,userId):
        try:
            query = ("CALL `aggiungiUtente`('"+str(userId)+"');")
            self.cursor.execute(query)
            self.database_connection.commit()
            return True
        except:
            return False

    def add_in_history_by_id(self,userId,incantesimo):
        try:
            query = ("CALL `aggiungiInCronologia`('"+str(userId)+"','"+incantesimo+"');")
            self.cursor.execute(query)
            self.database_connection.commit()
            return True;
        except:
            return False

    def remove_favourite(self,userId,incantesimo):
        try:
            query = ("CALL `rimuoviPreferiti`('"+str(userId)+"','"+incantesimo+"');")
            self.cursor.execute(query)
            self.database_connection.commit()
            return True;
        except:
            return False

    def get_favourite(self, idUser):
        query = ("CALL `ottieniPreferiti`('"+str(idUser)+"');")
        return self.get_query_result(query)

    def print_result(self,content):
        for tupla in content:
            for nomeColonna, valore in tupla.items():
                print(nomeColonna+" : "+str(valore))
    
    def get_spells_history(self, chat_id, limit):
        query = ("CALL ottieniCronologia('"+str(chat_id)+"','"+str(limit)+"');")
        return self.get_query_result(query)
    
    def get_users(self):
        query = ("CALL getUsers();")
        self.cursor.execute(query)
        content_list = []
        for row in self.cursor:
            content_list.append(row[0])
        return content_list