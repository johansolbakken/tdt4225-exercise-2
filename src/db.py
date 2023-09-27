import mysql.connector as mysql
import log


class DbConnector:
    """
    Connects to the MySQL server on the Ubuntu virtual machine.
    Connector needs HOST, DATABASE, USER and PASSWORD to connect,
    while PORT is optional and should be 3306.

    Example:
    HOST = "tdt4225-00.idi.ntnu.no" // Your server IP address/domain name
    DATABASE = "testdb" // Database name, if you just want to connect to MySQL server, leave it empty
    USER = "testuser" // This is the user you created and added privileges for
    PASSWORD = "test123" // The password you set for said user
    """

    def __init__(self,
                 HOST="tdt4225-16.idi.ntnu.no",
                 DATABASE="DATABASE_NAME",
                 USER="TEST_USER",
                 PASSWORD="test123"):
        # Connect to the database
        try:
            self.db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=3306)
        except Exception as e:
            log.error("Failed to connect to db:", e)

        # Get the db cursor
        self.cursor = self.db_connection.cursor()

        log.info(f"Connected to: {self.db_connection.get_server_info()}")
        # get database information
        self.cursor.execute("select database();")
        database_name = self.cursor.fetchone()
        log.info(f"You are connected to the database: {database_name}")

    def close_connection(self):
        # close the cursor
        self.cursor.close()
        # close the DB connection
        self.db_connection.close()
        log.info("Connection to %s is closed" % self.db_connection.get_server_info())
