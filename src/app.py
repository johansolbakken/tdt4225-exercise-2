import db
import queries
import log

logo = """
  _   _ _ _                 _____  ____  
 | \ | (_) |               |  __ \|  _ \ 
 |  \| |_| |__   __ _  ___ | |  | | |_) |
 | . ` | | '_ \ / _` |/ _ \| |  | |  _ < 
 | |\  | | | | | (_| | (_) | |__| | |_) |
 |_| \_|_|_| |_|\__,_|\___/|_____/|____/ 

"""

class App:
    def __init__(self):
        self.__running : bool = True
        self.__nuke : bool = False
        self.__dataset : str = ""
        self.__connector : db.DbConnector = db.DbConnector(
            HOST="localhost",
            DATABASE="example",
            USER="example",
            PASSWORD="example",
        )
        self.__cursor = self.__connector.cursor
        self.__db_connection = self.__connector.db_connection

    def __shutdown(self):
        self.__connector.close_connection()

    def run(self):
        print("NihaoDB v0.0.1-alpha")

        print(logo)

        if self.should_create_tables():
            self.create_tables()

        while self.__running:
            self.__running = False

        self.__shutdown()
    # 👹
    def nuke_database(self):
        try:
            self.__cursor.execute("DROP TABLE IF EXISTS trackpoint")
            self.__cursor.execute("DROP TABLE IF EXISTS activity")
            self.__cursor.execute("DROP TABLE IF EXISTS user")
        except Exception as e:
            log.error(f"Failed to nuke database. {e}")
            exit(1)
        log.success("Nuked database")

    def should_create_tables(self):
        if self.__nuke:
            return True

        self.__cursor.execute("SHOW TABLES")
        tables = self.__cursor.fetchall()
        if len(tables) != 3:
            return True
        return False
    
    def create_tables(self):
        self.nuke_database()
        self.__cursor.execute(queries.create_user_table)
        self.__cursor.execute(queries.create_activity_table)
        self.__cursor.execute(queries.create_trackpoint_table)
        log.success("Created tables")

    def set_dataset(self, dataset):
        self.__dataset = dataset

    def set_nuke(self, nuke):
        self.__nuke = nuke