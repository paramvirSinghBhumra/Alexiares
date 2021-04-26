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
        new_line = str(row)+ " " 
        new_line = str(new_line.replace("'", "").replace("(", "").replace(")", ""))
        # print(new_line)
        arr.append(new_line.split(', '))
    
    for row in arr:
        row[-1] = row[-1].replace(" ","")
    
    return arr

# converts the data into a json format with the appropriate headdings 
def make_JSON(col_names, values):
    everything = []
    for val in values:
        dict = {t:s for t,s in zip(col_names, val)}
        everything.append(dict)
    return everything


def second_order_nextLevel(cursor, name, id, second=True):
    new_name = ""
    if name == "Subsystem":
        new_name = "System"
        sql = 'SELECT "id", "System_id" FROM DBADMIN."{0}" WHERE "id" = {1};'.format(name, id)
        # print("*", sql, "*")
        cursor.execute(sql)
        arr = make_ARR(cursor)

    if name == "System":
        new_name = "Site"
        sql = 'SELECT "id", "Site_id" FROM DBADMIN.\"{0}\" WHERE \"id\" = {1};'.format(name, id)
        cursor.execute(sql)
        arr = make_ARR(cursor)

    if name == "Site":
        return []
        new_name = "Mission"

    arr2 = []
    dict = {
        "Subsystem": "System_id",
        "System":"Site_id",
        "Site":"id" #for now!
        }


    for id in [a1[1] for a1 in arr]:
        sql = 'SELECT "id", "{0}" FROM DBADMIN."{1}" WHERE "id" = {2};'.format(dict[new_name],new_name, id)
        cursor.execute(sql)
        temp_arr = make_ARR(cursor)
        arr2+=(temp_arr)


    for a in arr2:
        a.insert(0,new_name)
        a.insert(0,'2' if second else '3')
    
    return arr2

def second_order(cursor, name, id, second=True):
    #second order effect
    cursor.callproc('"DBADMIN"."SPECIFIC1_{}"'.format(name), (id, '?'))
    arr = make_ARR(cursor)
    for a in arr:
        a.insert(0,name)
        a.insert(0,'2' if second else '3')


    return arr



def third_order(cursor, name, id):
    #third order effect
    cursor.callproc('"DBADMIN"."SPECIFIC2_{}"'.format(name), (id, '?'))
    arr = make_ARR(cursor)
    for a in arr:
        a.insert(0, name)
        a.insert(0, '3') 
    return arr

def third_order_nextLevel(cursor, name, id, arr2):
    final_array = []
    for a in arr2:
        temp1_arr = second_order_nextLevel(cursor, a[1], a[2], second=False)
        final_array+= temp1_arr
        #different level
        if name != a[1]:
            temp2_arr = second_order(cursor, a[1], a[2], second=False)
            final_array+= temp2_arr
    return(final_array)
    return []

#each function returns a JSON
class True_View:
    def __init__(self):
        self.store = HANAStore()
        self.conn = self.store.get_connection()
        self.cursor = self.conn.cursor()
    
    def get_ALL(self, name):
        sql = 'SELECT * FROM DBADMIN."{}";'.format(name)
        # sql = 'SELECT "id", "Site_id" FROM DBADMIN."System" WHERE "id" = 1;'
        self.cursor.execute(sql) 
        arr = make_ARR(self.cursor)
        col_names = get_columnNames(self.cursor, name)
        return make_JSON(col_names, arr)

    def get_Specific(self, name, id):

        if name == "Mission" or name == "Site" or name == "System" or name == "Subsystem":
            col_names = ['order_effect', 'asset_type', 'effectedNode_id', 'parentSystem_id']
            arr2_sameLevel = second_order(self.cursor, name, id)
            arr2_nextLevel = [] if name == "Site" or name == "Mission" else second_order_nextLevel(self.cursor, name, id) #done except for "Site"
            arr2 = arr2_sameLevel+arr2_nextLevel
            json2 = make_JSON(col_names, arr2)
            # print("json2 ", json2)


            arr3_sameLevel = third_order(self.cursor, name, id)
            arr3_nextLevel = [] if name == "Site" or name == "Mission" else third_order_nextLevel(self.cursor, name, id, arr2)
            arr3 = arr3_sameLevel+arr3_nextLevel
            json3 = make_JSON(col_names, arr3)
            # print("json3 ", json3)


            arr = arr2+arr3
            return make_JSON(col_names, arr)
        
        return {'error':'invalid <asset_name> for API call'}
        

    def __del__(self):
        self.cursor.close()
        self.conn.close()



if __name__ == "__main__":
    subsystem_id = 1
    tv = True_View()
    jsonn = tv.get_Specific("System", subsystem_id)
    print(jsonn)

    del tv
    