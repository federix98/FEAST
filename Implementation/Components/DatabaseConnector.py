import mysql.connector
import time

from Connector import Connector

class DatabaseConnector(Connector):
    def __init__(self, HOST, USER, PASS, DB, target_table = "sensor_data"):
        super().__init__()
        self.HOST = HOST
        self.USER = USER
        self.PASS = PASS
        self.DB = DB
        self.target_table = target_table
        self.last_id = -1
        print("Database connector to", self.DB, "created")

    def connect(self):
        self.connector = mysql.connector.connect(
                                        host=self.HOST,
                                        user=self.USER,
                                        password=self.PASS,
                                        database=self.DB
                                    )

    def send(self, message):
        db_cursor = self.connector.cursor()
        sql = "INSERT INTO " + str(self.target_table) + " (content) VALUES (%s)"
        db_cursor.execute(sql, (message,))
        self.connector.commit()
        db_cursor.close()

    def __checkNewData(self, mydb, last_id=-1):
        # print(mydb)
        iot_db_cursor = mydb.cursor(buffered=True)
        iot_db_cursor.execute("SELECT MAX(ID) FROM " + str(self.target_table) + "")
        mydb.commit()
        res_id = iot_db_cursor.fetchall()[0][0]
        if res_id == None:
            return None, last_id
        last_inserted_id = res_id
        #print("Local_id ", last_id)
        content = None
        if(last_inserted_id > last_id):
            #print("New data found ")
            iot_db_cursor.execute("SELECT content FROM " + str(self.target_table) + " where ID > " + str(last_id))
            mydb.commit()
            content = iot_db_cursor.fetchall()
        # else:
        #     print("No updates")

        iot_db_cursor.close()
        return content, last_inserted_id

    def receive(self):
        time.sleep(0.5)
        results, self.last_id = self.__checkNewData(self.connector, self.last_id)
        if results == None:
            #print("No new data")
            return None
        #print(results)
        else:
            return [row[0] for row in results]
        
