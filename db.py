import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv
load_dotenv()

class Connect:
    def __init__(self):
        self.dbconfig = {
            "host": os.getenv("dbhost"),
            "user": os.getenv("user"),
            "password": os.getenv("password"),
            "database": os.getenv("database")
        }
        self.cnxpool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name = "mypool",
            pool_size = 10,
            pool_reset_session = True,
            **self.dbconfig
        )
    def get_all_photos(self):
        try:
            sql = f"""
                SELECT photo_name, url, created_time
                FROM photos
            """
            # connect to database
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor(buffered = True)
            # execute query
            self.cur.execute(sql)
            self.result = self.cur.fetchall()
            # close database connection
            self.cur.close()
            self.cnx.close()
            return self.result
        except Exception as e:
            print(e, "ERROR in db.Connect.query()")
            return "MySQL connection error"
    def insert(self, name):
        try:
            url = "https://do0ekvbuv8ir8.cloudfront.net/" + name
            sql = f"""
                INSERT INTO photos (photo_name, url)
                VALUES ('{name}', '{url}')
            """
            # connect to database
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor(buffered = True)
            # execute query
            self.cur.execute(sql)
            self.cnx.commit()
            # close database connection
            self.cur.close()
            self.cnx.close()
            return "insert success"
        except Exception as e:
            print(e, "ERROR in db.Connect.insert()")
            return "MySQL connection error"
    def delete(self, key):
        try:
            sql = f"""
                DELETE FROM photos
                WHERE photo_name = '{key}'
            """
            # connect to database
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor(buffered = True)
            # execute query
            self.cur.execute(sql)
            self.cnx.commit()
            # close database connection
            self.cur.close()
            self.cnx.close()
            return "delete success"
        except Exception as e:
            print(e, "ERROR in db.Connect.insert()")
            return "MySQL connection error"