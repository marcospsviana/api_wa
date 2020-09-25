import os
import sqlite3
import mysql.connector as mdb
import json

class DataAccessDB:
    def __init__(self):
        self.__host = 'localhost'
        self.__user = 'root'
        self.__passwd = 'microat8501'
        self.__db = 'worldangels'
        self.__conn =  mdb.connect(host='localhost', user='root', password='microat8051', database='worldangels') #sqlite3.connect('offerservice.db')
        self.__cursor = self.__conn.cursor()
        
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS `worldangels`.`tb_user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `idUser` TEXT(1245) NULL,
  `avatarUrl` TEXT(1245) NULL,
  `name` TEXT(145) NULL,
  `email` TEXT(145) NULL,
  `categories` TEXT(85) NULL,
  `subcategories` TEXT(85) NULL,
  `description` TEXT(245) NULL,
  `likes` INT(10) NULL,
  `dislikes` INT(10) NULL,
  `total_votos` INT(15) NULL,
  `localization` JSON NULL,
  `price` FLOAT NULL,
  `saves` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`photos`)),
  `photos` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`photos`)),
  PRIMARY KEY (`id`));"""
            )
        #self.__cursor.execute("""CREATE TABLE IF NOT EXISTS `worldangels`.`tb_saves` (
        #     `id` INT NOT NULL AUTO_INCREMENT,
        #      `id_user` INT NOT NULL,
        #      `idUser` TEXT(1245) NULL,
        #      PRIMARY KEY (`id`),
        #      CONSTRAINT `fk_tb_saves_1`
        #      FOREIGN KEY (`id_user`)
        #      REFERENCES `worldangels`.`tb_user` (`id`)
        #      ON DELETE CASCADE
        #      ON UPDATE CASCADE);""")
            
#        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS `worldangels`.`tb_searchprof` (
#  `id` INT NOT NULL,
#  `idUser` TEXT(1245) NULL,
#  `categories` VARCHAR(45) NULL,
#  `subcategories` VARCHAR(45) NULL,
#  `description` TEXT(1245) NULL,
#  `localization` JSON NULL,
#  `price` DECIMAL NULL,
#  PRIMARY KEY (`id`),
#  CONSTRAINT `fk_tb_searchprof_1`
#    FOREIGN KEY (`id`)
#    REFERENCES `worldangels`.`tb_user` (`id`)
#    ON DELETE CASCADE
#    ON UPDATE CASCADE);
#""")
     
     
#     self.__cursor.execute("""CREATE TABLE IF NOT EXISTS `worldangels`.`tb_photos_portfolio` (
#  `id_photos` int(11) NOT NULL AUTO_INCREMENT,
#  `idUser` TEXT(1245) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#  `photos` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`photos`)),
#  PRIMARY KEY (`id_photos`)
#) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;""")



#    def db_passwd(self):
#        return self.__passwd


#    def db_user(self):
#        return self.__user


#    def db_host(self):
#        return self.__host

#    def db_database(self):
#        return self.__db
    
    @classmethod
    def db_conn(self):
        self.__conn =  mdb.connect(host='localhost', user='root', password='microat8051', database='worldangels')
        return self.__conn
    
    @classmethod
    def cadastro_user(self, data):
        __conn =  mdb.connect(host='localhost', user='root', password='microat8051', database='worldangels')
        __cursor = __conn.cursor()
        print(data['localization'])
        __cursor.execute("""
            INSERT INTO tb_user (id,idUser,avatarUrl,name,email,categories,subcategories,description,likes,dislikes,total_votos,localization,price,saves, photos) VALUES (null, '%s', null, '%s','%s', '%s', '%s','%s', 0, 0, 0,'{"localization":{"%s","%s","%s"}',0,null,null)
            """%(data['idUser'],data['name'],data['email'],data['categories'],data['subCategories'],data['description'],data['localization'][0],data['localization'][1],data['localization'][2]))
        __conn.commit()
    
    @classmethod
    def cadastro_photos_user(self, idUser, key_number, dados):
        print("dados --- dadatabva")
        print(dados)
        print("idUser ----> %s"%idUser)
        print(" ------ fim dados ------")
        __conn =  mdb.connect(host='localhost', user='root', password='microat8051', database='worldangels')
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
        __cursor.execute("""UPDATE tb_user SET photos = JSON_INSERT(photos, '$.%s', "%s") WHERE idUser = '%s'"""%(key_number, dados, idUser))
        __conn.commit()
    
    @classmethod
    def delete_photos_user(self, idUser, key_number):
        print("idUser, key_number  ===> %s , %s"%(idUser, key_number))
        __conn =  mdb.connect(host='localhost', user='root', password='microat8051', database='worldangels')
        __cursor = __conn.cursor()
        __cursor.execute("SELECT idUser from tb_user where idUser = '%s'"%idUser)
        response = __cursor.fetchall()
        print("response %s"%response)
        if response == None or response == '' or response == []:
            return ("não há foto com estes dados")
        else:
            __cursor.execute("""UPDATE tb_user SET photos = JSON_REMOVE(photos, '$.%s') WHERE idUser = '%s'"""%(key_number, idUser))
            __conn.commit()
    
    @classmethod
    def get_category(self, category):
        __conn =  mdb.connect(host='localhost', user='root', password='microat8051', database='worldangels')
        __cursor = __conn.cursor()
        __cursor.execute("SELECT * from tb_user where categories = '%s'"%category)
        return __cursor.fetchall()
