
import db

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

        while self.__running:
            print(self.__dataset)
            self.__running = False

        self.__shutdown()

    def set_dataset(self, dataset):
        self.__dataset = dataset