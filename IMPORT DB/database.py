import mysql.connector
from mysql.connector import errorcode

class Database:

    def __init__(self, cursor):
        self.mycursor = cursor

    def use_database(self, dbname):
        try:
            self.mycursor.execute("USE {};".format(dbname))

        except mysql.connector.Error as error:
            print("Database {} does not exists".format(dbname))
            if error.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(dbname)
                print("Database {} created successfully".format(dbname))
        else:
            print("\t USE OK")

    def create_database(self, dbname):
        try:
            req = ("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8';".format(
                dbname))
            self.execute_request(req)
        except mysql.connector.Error as error:
            print("Failed creating database: {}".format(error))
            exit(1)
        else:
            print("\t CREATION DB Ok")
            self.use_database(dbname)

    def remove_database(self, dbname):
        try:
            req = ("DROP DATABASE {}".format(
                dbname))
            self.execute_request(req)
        except mysql.connector.Error as error:
            print("Failed deleting database: {}".format(error))
            exit(1)
        else:
            print("\t DELETION DB Ok")

    def create_tables(self, tables, database):
        for table_name in tables:
            print("###### " + table_name + " ######")
            table_description = tables[table_name]
            try:
                print("\t Table : {} ...".format(table_name), end='')
                self.execute_request(table_description)
            except mysql.connector.Error as error:
                if error.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(error.msg)
            else:
                print("\t CREATION TABLE Ok")
                database.commit()

    def execute_request(self, req):

        try:
            self.mycursor.execute(req)
        except Exception as error:
            print("Incorrect SQL query: \n {} \n Detected error : ".format(
                req))
            print(error)
            return 0
        else:
            return 1