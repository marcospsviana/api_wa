# -*- coding: utf-8 -*-
import os
import sqlite3
import mysql.connector as mdb
import json
import pandas as pd
import collections
from datetime import datetime

class DataAccessDB:
    
    def __init__(self):
        self.__host = 'localhost'
        self.__user = 'root'
        self.__passwd = 'microat8501'
        self.__db = 'worldangels'
        self.__conn =  mdb.connect(host='localhost', user='root', password='microat8051', database='worldangels') #sqlite3.connect('offerservice.db')
        self.__cursor = self.__conn.cursor()
        
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS `worldangels`.`tb_user_json` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `user` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`user`)),
             PRIMARY KEY (`id`));""")
            
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS `tb_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idUser` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `avatarUrl` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`avatarUrl`)),
  `name` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `categories` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `subcategories` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `likes` int(10) DEFAULT NULL,
  `dislikes` int(10) DEFAULT NULL,
  `totalVotos` int(15) DEFAULT NULL,
  `localization` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `price` float DEFAULT NULL,
  `saves` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `photos` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dateRegister` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"""
            )
        
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS worldangels.tb_depoimentos (
	id BIGINT auto_increment NULL,
	idUser TEXT NOT NULL,
	depoimentos LONGTEXT NOT NULL,
	likes BIT DEFAULT 0 NULL,
	dislike BIT DEFAULT 0 NULL,
	PRIMARY KEY (id)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;""")
        
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS worldangels.tb_chat (
	id_chat BIGINT auto_increment NOT NULL,
	idUser TEXT NOT NULL,
	`from` varchar(100) NULL,
	`to` varchar(100) NULL,
	message LONGTEXT NULL,
	PRIMARY KEY (id_chat)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;""")
        
        
        
    @classmethod
    def db_conn(self):
        self.__conn =  mdb.connect(host='localhost', user='root', password='microat8051', database='worldangels')
        return self.__conn
    
    @classmethod
    def receive_chat(self, idUser):
        print("id user em receive_chat %s"%idUser)
        data_array = []
        __conn =  self.db_conn()
        __cursor = __conn.cursor()
        __cursor.execute(""" SELECT * FROM tb_chat where  id_chat in (select MAX(id_chat) from tb_chat where idUserSender = '%s' group by idUserReceiver);"""%idUser)
        #__cursor.execute("""select *  from tb_chat where idUserSender = "%s" group by idUserReceiver  ORDER BY (date) ASC"""%(idUser))
        #__cursor.execute("""select * , COUNT(idUserSender) from tb_chat where idUserSender = '%s' or idUserReceiver = '%s' group by id_chat HAVING COUNT(idUserSender) > 0 ORDER BY (date) ASC;"""%(idUser, idUser))
        response = __cursor.fetchall()
        #print("response in data access %s "%response)
        for r in response:
            d = collections.OrderedDict()
            d["id_chat"] = r[0]
            d["idUserSender"] = r[1]
            d["idUserReceiver"] = r[2]
            d["message"] = r[3]
            d["date_message"] = r[4]
            data_array.append(d)
        
        #data = json.dumps(data_array)
        return data_array
    @classmethod
    def receive_chat_unique(self, idUserReceiver):
        data_array = []
        __conn =  self.db_conn()
        __cursor = __conn.cursor()
        __cursor.execute(""" SELECT * FROM tb_chat WHERE (idUserSender = '%s' or idUserReceiver = '%s')"""%(idUserReceiver, idUserReceiver))
        #__cursor.execute("""select * from tb_chat where idUserSender = '%s' OR idUserReceiver = '%s' group by idUserReceiver having count(id_chat) > 0 ORDER BY (id_chat) ASC;"""%(idUser, idUser))
        #__cursor.execute("""select * , COUNT(idUserReceiver) from tb_chat where idUserSender = '%s' or idUserReceiver = '%s'  and date = (select max(date) from tb_chat) group by idUserReceiver HAVING #COUNT(idUserReceiver) > 0 ORDER BY (date) ASC;"""%(idUserReceiver, idUserReceiver))
        response = __cursor.fetchall()
        #print("response in data access %s "%response)
        for r in response:
            d = collections.OrderedDict()
            d["id_chat"] = r[0]
            d["idUserSender"] = r[1]
            d["idUserReceiver"] = r[2]
            d["message"] = r[3]
            d["date_message"] = r[4]
            data_array.append(d)
        
        #data = json.dumps(data_array)
        return data_array
    
    @classmethod
    def insert_chat(self, data):
        DIAS = [
            'Segunda-feira',
            'Terça-feira',
            'Quarta-feira',
            'Quinta-Feira',
            'Sexta-feira',
            'Sábado',
            'Domingo'
              ]
        data_calendar = datetime.now()
        date=data_calendar
        weekday_name = DIAS[data_calendar.weekday()]
        data_calendar = "{} {}:{} {}-{}-{}".format(weekday_name, data_calendar.hour, data_calendar.minute, data_calendar.day, data_calendar.month, data_calendar.year)
        
        __conn = self.db_conn()
        __cursor = __conn.cursor()
        __cursor.execute("""
            INSERT INTO worldangels.tb_chat (id_chat,idUserSender, idUserReceiver, message, date_message, date) VALUES( null,'%s', '%s', '%s', '%s', '%s')"""%(data['idUserSender'],data['idUserReceiver'],data['message'],data_calendar, date))
        __conn.commit()
    
    @classmethod
    def cadastro_user(self, data):
        data_calendar = datetime.now()
        __conn = self.db_conn()
        __cursor = __conn.cursor()
        print(data['localization'])
        __cursor.execute("""
        INSERT INTO tb_user (id,idUser,avatarUrl,name,email,categories,subcategories,description,likes,dislikes,totalVotos,localization,price,saves, photos) VALUES (null, '%s', null, '%s','%s', '%s', '%s','%s', 0, 0, 0,'%s,%s','%s',null,null, '%s')"""%(data['idUser'],data['name'],data['email'],data['categories'],data['subCategories'],data['description'],data['localization'][1],data['localization'][2],data['price'], data_calendar))
       # __cursor.execute(""" INSERT INTO tb_user_json (id, user) VALUES ( null, '{"user":'%s'}') """%data)
        __conn.commit()
    
    @classmethod
    def cadastro_photos_user(self, idUser, dados):
        print("dados --- dadatabva")
        print(dados)
        print("idUser ----> %s"%idUser)
        print(" ------ fim dados ------")
        __conn = self.db_conn()
        __cursor = __conn.cursor()
        #__cursor.execute("SELECT id_photos from tb_photos_portfolio where idUser = '%s'"%idUser)
        #response = __cursor.fetchall()
        #print("response %s"%response)
        #if response == None or response == '' or response == []:
         #   __cursor.execute("""INSERT INTO tb_photos_portfolio(id_photos, idUser, photos) VALUES (NULL, '%s', '{"photos":{"%s":"%s"}}')"""%(idUser,key_number, dados))
          #  __conn.commit()
        #else:
          #  __cursor.execute("""UPDATE tb_photos_portfolio photos SET @photos = "$.%s", '{"%s"}') WHERE idUser = '%s'"""%(key_number, dados, idUser))
          #  __conn.commit()
        __cursor.execute("UPDATE tb_user SET photos = '%s' WHERE idUser = '%s'"%(dados, idUser))
        __conn.commit()
    
    @classmethod
    def delete_photos_user(self, idUser, key_number):
        print("idUser, key_number  ===> %s , %s"%(idUser, key_number))
        __conn = self.db_conn()
        __cursor = __conn.cursor()
        __cursor.execute("SELECT idUser from tb_user where idUser = '%s'"%idUser)
        response = __cursor.fetchall()
        print("response %s"%response)
        if response == None or response == '' or response == []:
            return ("não há foto com estes dados")
        else:
            __cursor.execute("""UPDATE tb_user SET photos = '%s' WHERE idUser = '%s'"""%(key_number, idUser))
            __conn.commit()
    
    @classmethod
    def get_category(self, category):
        __conn = self.db_conn()
        __cursor = __conn.cursor()
        __cursor.execute("SELECT * from tb_user where categories = '%s'"%category)
        #sql = "SELECT * from tb_user"
        #result = pd.read_sql(sql, __conn)
        #result_json = result.to_json(orient="index")
        #parsed = json.loads(result_json)
        response = __cursor.fetchall()
        #return parsed
        array_response = []
        data = {}
        d = collections.OrderedDict()
        for r in response:
            d = collections.OrderedDict()
            #d["id"] = r[0]
            d["idUser"] = r[1]
            d["avatarUrl"] = r[2]
            d["name"] = r[3]
            d["email"] = r[4]
            d["categories"] = r[5]
            d["subCategories"] = r[6]
            d["description"] = r[7]
            d["likes"] = r[8]
            d["dislikes"] = r[9]
            d["totalVotos"] = r[10]
            d["localization"] = r[11]
            d["price"] = r[12]
            d["saves"] = r[13]
            d["photos"] = r[14]
            d["dateRegister"] = r[15]
            if d["totalVotos"] == 0:
                d["totalVotos"] = 1
            d["rate"] = d["likes"] / d["totalVotos"]
            array_response.append(d)
            print(" total votos %d" %d["totalVotos"])
        dados = json.dumps(array_response) 
        return dados
    
    @classmethod
    def avatar(self,filename_path, destination):
        __conn = self.db_conn()
        __cursor = __conn.cursor()
        __cursor.execute("""UPDATE tb_user SET avatarUrl = '%s'  WHERE idUser = '%s'"""%(destination, filename_path))
        __conn.commit()
    
    @classmethod
    def get_user_profile(self, idUser):
        __conn = self.db_conn()
        __cursor = __conn.cursor()
        __cursor.execute("SELECT name, avatarUrl, categories, subCategories, description, likes, dislikes, totalVotos, localization, price, photos, dateRegister FROM tb_user where idUser = '%s'"%(idUser))
        response = __cursor.fetchall()
        array_response = []
        dados = {}
        
        for r in response:
            d = collections.OrderedDict()
            d["name"] = r[0]
            d["avatarUrl"] = r[1]
            d["categories"] = r[2]
            d["subCategories"] = r[3]
            d["description"] = r[4]
            d["likes"] = r[5]
            d["dislikes"] = r[6]
            d["totalVotos"] = r[7]
            d["localization"] = r[8]
            d["price"] = r[9]
            d["photos"] = r[10]
            d["dateRegister"] = r[11]
            if d["totalVotos"] == 0:
                d["totalVotos"] = 1
            d["rate"] = d["likes"] / d["totalVotos"]
            array_response.append(d)
            
        dados = json.dumps(array_response)
        return dados
    
    
    @classmethod
    def get_saves(self, idUser):
        __conn = self.db_conn()
        __cursor = __conn.cursor()
        saves = tuple(idUser)
        where_clause = ",".join(["%s"]*len(idUser))
        query = """SELECT name, avatarUrl, categories, subCategories, description, likes, dislikes, totalVotos, localization, price, photos FROM `tb_user` where `idUser` in ({}) group by name"""
        query = query.format(where_clause)
        print(query)
        print(idUser)
        #s = ''
        #args = (saves,)
        #__cursor.execute("""SELECT name, avatarUrl, categories, subCategories, description, likes, dislikes, totalVotos, localization, price, photos, dateRegister, FROM tb_user where idUser in %s;"""% (saves,))
        #sql_query = 'SELECT name, avatarUrl, categories, subCategories, description, likes, dislikes, totalVotos, localization, price, photos, dateRegister FROM tb_user where idUser IN (" ",%s)' % ','.join(map(str, saves)) 
        #__cursor.execute("SELECT name, avatarUrl, categories, subCategories, description, likes, dislikes, totalVotos, localization, price, photos, dateRegister, FROM tb_user where idUser in ({', '.join(s for s in saves })"%(saves))
        __cursor.execute(query, idUser)
        #__cursor.execute('SELECT name, avatarUrl, categories, subCategories, description, likes, dislikes, totalVotos, localization, price, photos, dateRegister FROM tb_user where idUser in ?'%(saves,))
        response = __cursor.fetchall()
        
        array_response = []
        
        dados = {}
        for r in response:
            d = collections.OrderedDict()
            d["name"] = r[0]
            d["avatarUrl"] = r[1]
            d["categories"] = r[2]
            d["subCategories"] = r[3]
            d["description"] = r[4]
            d["likes"] = r[5]
            d["dislikes"] = r[6]
            d["totalVotos"] = r[7]
            d["localization"] = r[8]
            d["price"] = r[9]
            d["photos"] = r[10]
            #d["dateRegister"] = r[11]
            if d["totalVotos"] == 0:
                d["totalVotos"] = 1
            d["rate"] = d["likes"] / d["totalVotos"]
            array_response.append(d)
            
        dados = json.dumps(array_response)
        return dados
    
    @classmethod
    def get_user_depoimentos(self, idUser):
        __conn = self.db_conn()
        __cursor = __conn.cursor()
        __cursor.execute("SELECT * FROM tb_depoimentos where idUser = '%s'"%(idUser))
        response = __cursor.fetchall()
        array_response = []
        dados = {}
        for r in response:
            d = collections.OrderedDict()
            d["titulo"] = r[2]
            d["depoimentos"] = r[3]
            d["likes"] = r[4]
            d["dislike"] = r[5]
            array_response.append(d)
        dados = json.dumps(array_response)
        return dados
    
    @classmethod
    def set_user_depoimentos(self, depoimentos):
        __conn = self.db_conn()
        __cursor = __conn.cursor()
        __cursor.execute("INSERT INTO tb_depoimentos (id, idUser, titulo, depoimentos, likes, dislike) values (null, %(idUser)s, %(titulo)s, %(depoimentos)s, %(likes)s, %(dislike)s)", ({"idUser": depoimentos['idUser'], "titulo": depoimentos['titulo'], "depoimentos":depoimentos['depoimentos'], "likes":depoimentos['likes'], "dislike":depoimentos['dislike']}))
        response = __cursor.fetchall()
        array_response = []
        dados = {}
        for r in response:
            d = collections.OrderedDict()
            d["titulo"] = r[2]
            d["depoimentos"] = r[3]
            d["likes"] = r[4]
            d["dislike"] = r[5]
            array_response.append(d)
        dados = json.dumps(array_response)
        return dados
    
    @classmethod
    def get_avatar(self, idUser):
        """ retorna o link do avatar do usuario tipo de dado String"""
        __conn = self.db_conn()
        __cursor = __conn.cursor()
        __cursor.execute("SELECT avatarUrl FROM tb_user where idUser = '%s'"%(idUser))
        response = __cursor.fetchone()
        print("RESPONSE EM GET_AVATAR %s"%response)
        if response == None:
            response = "/static/images/avatar_default.png"
            return response
        else:
            print("response puro %s"%response)
            return response
        
        
        
    
    @classmethod
    def get_user_category(self, idUser):
        __conn = self.db_conn()
        __cursor = __conn.cursor()
        __cursor.execute(""" SELECT name, categories FROM tb_user where idUser = '%s'"""%idUser)
        response = __cursor.fetchall()
        print("response get_user_category %s"%response)
        return response
        

        
