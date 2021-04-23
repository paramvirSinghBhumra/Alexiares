# class HANAStore:
#     def __init__(self):
#         #in login_credentials file
#         self.host = "temp"
#         self.port = "temp"
#         self.user = "temp"
#         self.pwd = "temp"


#     def get_connection(self):
#         conn = dbapi.connect(
#             address=self.host,
#             port=self.port,
#             user=self.user,
#             password=self.pwd,
#             encrypt=True,
#             sslValidateCertificate=False
#         )
#         return conn

#example
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
