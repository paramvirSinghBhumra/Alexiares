from hdbcli import dbapi
import json
import uuid
from datetime import datetime

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

#example
class Airport:
    def __init__(self):
        self.store = HANAStore()
        self.conn = self.store.get_connection()
        self.cursor = self.conn.cursor()

    def get_ALL(self):
        sql = "SELECT * FROM AIRPORTS;"
        self.cursor.execute(sql)

        for row in self.cursor:
            print(row)
    
    def Airport_PossibleRoutes(self):
        sql = "CALL DBADMIN.SP_TravelPossible('NTE', 'PDX', ?);" # <- doesnt work!
        self.cursor.execute(sql) # <- execute SQL 

    def Airport_TripRouting(self):
        self.cursor.callproc('DBADMIN.SP_TripRouting', ('NTE', 'PDX', '?', '?', '?', '?'))
        for row in self.cursor:
            print(row)
        # sql = "CALL DBADMIN.SP_TripRouting('NTE', 'PDX', ?, ?, ?, ?);"
        # cursor.execute(sql)

if __name__ == "__main__":
    airport = Airport()
    # airport.get_ALL()
    airport.Airport_TripRouting()