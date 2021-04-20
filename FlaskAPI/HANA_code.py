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
        # self.host =
        # self.port = 
        # self.user = 
        # self.pwd = 
        self.host = 'c18c36bc-5d5b-4d0f-9ef6-99e1ea023bb8.hana.prod-us10.hanacloud.ondemand.com'
        self.port = '443'
        self.user = 'DBADMIN'
        self.pwd = 'N0radNorthcom'

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
    SELECT COLUMN_NAME FROM TABLE_COLUMNS WHERE TABLE_NAME = :name;
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


class Airport:
    def __init__(self, store,conn,cursor):
        self.store = store
        self.conn = conn
        self.cursor = cursor

    def get_ALL(self):
        sql = "SELECT * FROM AIRPORTS;"
        self.cursor.execute(sql)
    
    def Airport_PossibleRoutes(self):
        sql = "CALL DBADMIN.SP_TravelPossible('NTE', 'PDX', ?);" # <- doesnt work!
        self.cursor.execute(sql) # <- execute SQL 

    def Airport_TripRouting(self):
        self.cursor.callproc('DBADMIN.SP_TripRouting', ('NTE', 'PDX', '?', '?', '?', '?'))
        # sql = "CALL DBADMIN.SP_TripRouting('NTE', 'PDX', ?, ?, ?, ?);"
        # cursor.execute(sql)


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


    




# if __name__ == '__main__':
#     store = HANAStore()
#     conn = store.get_connection()
#     cursor = conn.cursor()


#     col_names = get_columnNames(cursor, "AIRPORTS")
#     airports = Airport(store, conn, cursor)
#    # CARBON(store, conn, cursor)

#     #print values returned by calling procedure / SQL 
#     airports.get_ALL()
#     arr = []
#     for row in cursor:
#         new_line = str(row)+ " " 
#         new_line = str(new_line.replace("'", "").replace("(", "").replace(")", ""))
#         arr.append(new_line.split(', ')[:-1])
    
#     # print(arr)

#     total_airports = []
#     for airport in arr:
#         dict = {t:s for t,s in zip(col_names, airport)}
#         total_airports.append(dict)
#     print (json.dumps(total_airports))
    

    


#     cursor.close()
#     conn.close()


if __name__ == "__main__":
    tv = True_View()
    jsonn = tv.get_ALL("Site")
    del tv

    print(jsonn)
    