from data.data_access_db import DataAccessDB as DataDB
class DataAccesObjects(object):
    def __init__(self):
        self.__data = DataDB()
        
    def cadastro_user(self, dados):
        self.__data.cadastro_user(dados)
        
        
    def cadastro_photos_user(self, id, dados):
        self.__data.cadastro_photos_user(id, dados)
    
    
    def delete_photos_user(self, idUser, key_number):
        self.__data.delete_photos_user(idUser, key_number)
    
    def get_category(self, data):
        retorno = self.__data.get_category(data)
        return retorno
    
    def avatar(self,filename_path, destination):
        self.__data.avatar(filename_path, destination)
    
    def get_user_depoimentos(self, idUser):
        retorno = self.__data.get_user_depoimentos(idUser)
        return retorno
    
    def set_user_depoimentos(self, depoimento):
        retorno = self.__data.set_user_depoimentos(idUser)
        return retorno
    
    def insert_chat(self, data):
        retorno = self.__data.insert_chat(data)
        
    def get_avatar(self, idUser):
        response = self.__data.get_avatar(idUser)
        return response
    
    
    def receive_chat(self, idUser):
        response = self.__data.receive_chat(idUser)
        return response
    
    def get_user_category(self, idUser):
        response = self.__data.get_user_category(idUser)
        return response
    
    def receive_chat_unique(self, idUserReceiver):
        retorno = self.__data.receive_chat_unique(idUserReceiver)
        return retorno
    
    def get_saves(self, idUser):
        retorno = self.__data.get_saves(idUser)
        return retorno

        
