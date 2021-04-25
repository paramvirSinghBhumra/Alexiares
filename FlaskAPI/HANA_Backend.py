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
        # self.host = "temp"
        # self.port = "temp"
        # self.user = "temp"
        # self.pwd = "temp"
        
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


# automatically searches db and gets column names of table
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

# parses the result and converts it into an array
def make_ARR(cursor):
    arr = []
    for row in cursor:
        # arr.append(row)
        new_line = str(row)+ " " 
        new_line = str(new_line.replace("'", "").replace("(", "").replace(")", ""))
        arr.append(new_line.split(', '))
    
    return arr

# converts the data into a json format with the appropriate headdings 
def make_JSON(col_names, values):
    everything = []
    for val in values:
        dict = {t:s for t,s in zip(col_names, val)}
        everything.append(dict)
    return everything

def second_order(cursor, name, id, col_names):
    #second order effect
    cursor.callproc('"DBADMIN"."SPECIFIC1_{}"'.format(name), (id, '?'))
    arr = make_ARR(cursor)
    for a in arr:
        a.insert(0,name)
        a.insert(0,'2')
    print(arr)

    return arr

def third_order(cursor, name, id, col_names):
    #third order effect
    cursor.callproc('"DBADMIN"."SPECIFIC2_{}"'.format(name), (id, '?'))
    arr = make_ARR(cursor)
    for a in arr:
        a.insert(0, name)
        a.insert(0, '3') 

    print(arr)
    return arr

#each function returns a JSON
class True_View:
    def __init__(self):
        self.store = HANAStore()
        self.conn = self.store.get_connection()
        self.cursor = self.conn.cursor()
    
    def get_ALL(self, name):
        sql = 'SELECT * FROM DBADMIN."{}";'.format(name)
        self.cursor.execute(sql) 
        arr = make_ARR(self.cursor)
        col_names = get_columnNames(self.cursor, name)
        return make_JSON(col_names, arr)

    def get_Specific(self, name, id):

        if name == "Mission" or name == "Site" or name == "System" or name == "Subsystem":
            col_names = ['order_effect', 'asset_type', 'effectedNode_id', 'nextLevelEffected_id']
            arr2 = second_order(self.cursor, name, id, col_names)
            arr3 = third_order(self.cursor, name, id, col_names)
            
            arr = arr2+arr3
            return make_JSON(col_names, arr)
        
        return {'error':'invalid <asset_name> for API call'}
        

    def __del__(self):
        self.cursor.close()
        self.conn.close()



if __name__ == "__main__":
    subsystem_id = 1
    tv = True_View()
    tv.get_ALL("Subsystem")
    print(tv.get_Specific("Subsystem", subsystem_id))

    del tv
    