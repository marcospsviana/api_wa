from data.data_access_db import DataAccessDB as DataDB
class DataAccesObjects(object):
    def __init__(self):
        self._conn = DataDB.db_conn()
        self.data = DataDB()
        
    def cadastro_user(self, dados):
        self.data.cadastro_user(dados)
        
        
    def cadastro_photos_user(self, id, key_number, dados):
        self.data.cadastro_photos_user(id, key_number, dados)
    
    
    def delete_photos_user(self, idUser, key_number):
        self.data.delete_photos_user(idUser, key_number)
