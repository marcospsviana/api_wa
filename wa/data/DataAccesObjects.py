from data.data_access_db import DataAccessDB as DataDB
class DataAccesObjects(object):
    def __init__(self):
        self.__data = DataDB()
        
    def cadastro_user(self, dados):
        self.__data.cadastro_user(dados)
        
        
    def cadastro_photos_user(self, id, key_number, dados):
        self.__data.cadastro_photos_user(id, key_number, dados)
    
    
    def delete_photos_user(self, idUser, key_number):
        self.__data.delete_photos_user(idUser, key_number)
    
    def get_category(self, category):
        retorno = self.__data.get_category(category)
        return retorno
