import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

class obj:
    pass
    
class Spellbook:
    #Credenziali di accesso
    userName = None
    userPswd = None
    url = None
    dbName = None
    
    cn_object = None #Oggetto connessione al database
    cursor = None #Cursore ottenuto da cn_object

    def __init__(self,new_userName,new_userPswd,new_url,new_dbName):
        self.url = new_url
        self.userName = new_userName
        self.userPswd = new_userPswd
        self.dbName = new_dbName
        #Mi collego al database
        self.cn_object = MySQLdb.connect(self.url,
                                         self.userName,
                                         self.userPswd,
                                         self.dbName)
        self.cursor = self.cn_object.cursor()

    def __del__(self):
        self.cn_object.close()
        self.cursor.close()

    def ottieniIncantesimiDiLivello(self,lvl):
        query = ("CALL `ottieniIncantesimiDiLivello`('"+str(lvl)+"');")
        self.cursor.execute(query)
        contentList = []
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
            
            contentList.append(aux)
            aux = {}
        return contentList
    def ottieniIncantesimiPerClasseDiLivello(self,classe,lvl):
        query = ("CALL `ottieniIncantesimiPerClasseDiLivello`('"+classe+"','"+str(lvl)+"');")
        self.cursor.execute(query)
        contentList = []
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
            
            contentList.append(aux)
            aux = {}
        return contentList
    def ottieniIncantesimiPerClasse(self,classe):
        query = ("CALL `ottieniIncantesimiPerClasse`('"+classe+"');")
        self.cursor.execute(query)
        contentList = []
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
            
            contentList.append(aux)
            aux = {}
        return contentList
    def ottieniIncantesimiPerNome(self,nome):
        query = ("CALL `ottieniIncantesimiPerNome`('"+nome+"');")
        self.cursor.execute(query)
        contentList = []
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
            
            contentList.append(aux)
            aux = {}
        return contentList
    def aggiungiUtente(self,userId):
        try:
            query = ("CALL `aggiungiUtente`('"+str(userId)+"');")
            self.cursor.execute(query)
            self.cn_object.commit()
            return True
        except:
            return False
    def aggiungiPreferiti(self,userId,incantesimo):
        try:
            query = ("CALL `aggiungiPreferiti`('"+str(userId)+"','"+incantesimo+"');")
            self.cursor.execute(query)
            self.cn_object.commit()
            return True;
        except:
            return False
    def rimuoviPreferiti(self,userId,incantesimo):
        try:
            query = ("CALL `rimuoviPreferiti`('"+str(userId)+"','"+incantesimo+"');")
            self.cursor.execute(query)
            self.cn_object.commit()
            return True;
        except:
            return False
    def ottieniPreferiti(self, idUser):
        query = ("CALL `ottieniPreferiti`('"+str(idUser)+"');")
        self.cursor.execute(query)
        contentList = []
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
            
            contentList.append(aux)
            aux = {}
        return contentList
    def stampaRisultato(self,content):
        for tupla in content:
            for nomeColonna, valore in tupla.items():
                print(nomeColonna+" : "+str(valore))
        
        
'''
obj = Spellbook("standard","guruguru","localhost","dnd_5_incantesimi")

obj.stampaRisultato(obj.ottieniIncantesimiDiLivello(2))
obj.stampaRisultato(obj.ottieniIncantesimiPerNome("Ami"))

print(obj.aggiungiUtente(123456))
print(obj.aggiungiPreferiti(123456,"Amicizia"))
print(obj.rimuoviPreferiti(123456,"Amicizia"))
print(obj.aggiungiPreferiti(123456,"Amicizia"))
obj.stampaRisultato(obj.ottieniPreferiti(123456))
'''
