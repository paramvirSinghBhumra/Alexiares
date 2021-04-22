from hdbcli import dbapi
import json
import uuid
from datetime import datetime


# BACKEND SERVICE FOR API 
# go ahead with what we have right now. this won't work 
# to delip an api
# 1. you define your entitiy (vitutal table, cvs file)
#   a. within cvs file, define parameters of api you want 
#   b. upload file to website and it'll spit out a URL 


class HANAStore:
    def __init__(self):
        #in login_credentials file
        self.host = "temp"
        self.port = "temp"
        self.user = "temp"
        self.pwd = "temp"

    def get_connection(self):
        conn = dbapi.connect(
            address=self.host,
            port=self.port,
            user=self.user,
            password=self.pwd,
            encrypt=True,
            sslValidateCertificate=False
        )
        return conn

def get_columnNames(cursor, name):
    sql = """
    SELECT COLUMN_NAME FROM TABLE_COLUMNS WHERE TABLE_NAME = :name ORDER BY POSITION;
    """

    cursor.execute(sql, {"name":name})

    col_names = []
    for row in cursor:
        new_line = str(row)+ " " 
        new_line = str(new_line.replace("'", "").replace("(", "").replace(")", ""))
        col_names.append(new_line.split(', ')[0])
    
    return col_names

def make_ARR(cursor):
    arr = []
    for row in cursor:
        new_line = str(row)+ " " 
        new_line = str(new_line.replace("'", "").replace("(", "").replace(")", ""))
        arr.append(new_line.split(', ')[:-1])
    
    return arr


def make_JSON(col_names, values):
    everything = []
    for val in values:
        dict = {t:s for t,s in zip(col_names, val)}
        everything.append(dict)
    return everything


#each function returns a JSON
class True_View:
    def __init__(self):
        self.store = HANAStore()
        self.conn = self.store.get_connection()
        self.cursor = self.conn.cursor()
    
    def __helper(self, name):
        arr = make_ARR(self.cursor)
        col_names = get_columnNames(self.cursor, name)
        return make_JSON(col_names, arr)
    
    def get_ALL(self, name):
        sql = 'SELECT * FROM DBADMIN."{}";'.format(name)
        self.cursor.execute(sql) 
        return self.__helper(name)


    def __del__(self):
        self.cursor.close()
        self.conn.close()



if __name__ == "__main__":
    tv = True_View()
    jsonn = tv.get_ALL("Subsystem")
    del tv

    print(jsonn)
    