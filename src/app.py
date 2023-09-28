import db
import queries
import log
import model
import datetime
import os
import performance

logo = """
  _   _ _ _                 _____  ____  
 | \ | (_) |               |  __ \|  _ \ 
 |  \| |_| |__   __ _  ___ | |  | | |_) |
 | . ` | | '_ \ / _` |/ _ \| |  | |  _ < 
 | |\  | | | | | (_| | (_) | |__| | |_) |
 |_| \_|_|_| |_|\__,_|\___/|_____/|____/ 

"""

logo_with_colors = """
  _   _ _ _                \033[1;31m _____  \033[0m____  
 | \ | (_) |               \033[1;31m|  __ \\\033[0m|  _ \ 
 |  \| |_| |__   __ _  ___ \033[1;31m| |  | |\033[0m |_) |
 | . ` | | '_ \ / _` |/ _ \\\033[1;31m| |  | |\033[0m  _ < 
 | |\  | | | | | (_| | (_) \033[1;31m| |__| |\033[0m |_) |
 |_| \_|_|_| |_|\__,_|\___/\033[1;31m|_____/\033[0m|____/ 

"""

class App:
    def __init__(self):
        _ = performance.Timer("App init")

        print("NihaoDB v0.0.1-alpha")
        print(logo_with_colors)

        self.__running : bool = True
        self.__nuke : bool = False
        self.__use_small_dataset : bool = False
        self.__dataset : str = ""
        self.__cachefile : str = ".appcache/memcache.pkl"
        try:
            self.__connector : db.DbConnector = db.DbConnector(
                HOST="localhost",
                DATABASE="example",
                USER="example",
                PASSWORD="example",
            )
        except Exception as e:
            log.error(f"Failed to connect to database. {e}")
            exit(1)
        self.__cursor = self.__connector.cursor
        self.__db_connection = self.__connector.db_connection

    def __shutdown(self):
        _ = performance.Timer("App shutdown")
        self.__connector.close_connection()

    def run(self):
        if self.should_create_tables():
            _ = performance.Timer("App create tables")
            start = datetime.datetime.now()
            self.create_tables()
            if self.cache_exists():
                self.upload_data_from_cache()
            else:
                self.upload_data()
            end = datetime.datetime.now()
            log.success(f"Finished creating database and uploading files in {end - start}")

        while self.__running:
            self.__running = False

        self.__shutdown()
    # 👹
    def nuke_database(self):
        _ = performance.Timer("App nuke database")
        try:
            self.__cursor.execute("DROP TABLE IF EXISTS trackpoint")
            self.__cursor.execute("DROP TABLE IF EXISTS activity")
            self.__cursor.execute("DROP TABLE IF EXISTS user")
        except Exception as e:
            log.error(f"Failed to nuke database. {e}")
            exit(1)
        log.success("Nuked database")

    def should_create_tables(self):
        return True # 👹👹👹👹👹👹
        _ = performance.Timer("App should create tables")
        if self.__nuke:
            return True

        self.__cursor.execute("SHOW TABLES")
        tables = self.__cursor.fetchall()
        if len(tables) != 3:
            return True
        return False
    
    def create_tables(self):
        _ = performance.Timer("App create tables")
        if self.__nuke:
            self.nuke_database()
        self.__cursor.execute(queries.create_user_table)
        self.__cursor.execute(queries.create_activity_table)
        self.__cursor.execute(queries.create_trackpoint_table)
        log.success("Created tables")

    def upload_data(self, data=[]):
        _ = performance.Timer("App upload data")
        if not os.path.isdir(self.__dataset):
            log.warning(f"Dataset {self.__dataset} is not a directory (skipping uploading data)")
            return
        
        if data == []:
            data = model.generate_dataset(self.__dataset)
            _ = performance.Timer("Writing generated data to cache")
            model.write_dataset_to_cache(data, self.__cachefile)

        for (i,user) in enumerate(data):
            # if already exists, skip
            self.__cursor.execute("SELECT * FROM user WHERE id = %s", (user.id,))
            if self.__cursor.fetchone() is not None:
                continue

            percentage = (i+1)/len(data) * 100
            _ = performance.Timer(f"\tUploading data for user {user.id} ({percentage:.2f}%)")
        
            if user.has_label:
                self.__cursor.execute(queries.insert_user, (user.id, 1))
            else:
                self.__cursor.execute(queries.insert_user, (user.id, 0))

            for activity in user.activities:
                self.__cursor.execute(queries.insert_activity, (activity.id, activity.user_id, activity.transportation_mode, activity.start_date_time, activity.end_date_time))

                for trackpoint in activity.trackpoints:
                    self.__cursor.execute(queries.insert_new_trackpoint, (trackpoint.activity_id, trackpoint.lat, trackpoint.lon, trackpoint.altitude, trackpoint.date_days, trackpoint.date_time))
            self.__db_connection.commit()

    def set_dataset(self, dataset):
        self.__dataset = dataset

    def set_nuke(self, nuke):
        self.__nuke = nuke

    def set_small_dataset(self, small):
        self.__use_small_dataset = small

    def cache_exists(self):
        return os.path.exists(self.__cachefile)

    def upload_data_from_cache(self):
        data = model.load_dataset_from_cache(self.__cachefile)
        self.upload_data(data)