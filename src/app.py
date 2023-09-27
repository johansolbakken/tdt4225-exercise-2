import db
import queries
import log
import model
import datetime
import os

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
        print("NihaoDB v0.0.1-alpha")
        print(logo_with_colors)

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

        
        if self.should_create_tables():
            start = datetime.datetime.now()
            self.create_tables()
            self.upload_data()
            end = datetime.datetime.now()
            log.success(f"Finished creating database and uploading files in {end - start}")

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

    def upload_data(self):
        if not os.path.isdir(self.__dataset):
            log.warning(f"Dataset {self.__dataset} is not a directory (skipping uploading data)")
            return

        # Upload users
        log.info("Generating users data")
        start = datetime.datetime.now()
        users: list[model.User] = model.generate_users(self.__dataset)
        end = datetime.datetime.now()
        log.info(f"Generated users in {end - start}")
        log.info("Uploading users data")
        start = datetime.datetime.now()
        for user in users:
            if user.has_label:
                self.__cursor.execute(queries.insert_user, (user.id, 1))
            else:
                self.__cursor.execute(queries.insert_user, (user.id, 0))
        self.__db_connection.commit()
        end = datetime.datetime.now()
        log.success(f'Generated {len(users)} users in {end - start}')

        # Upload activities
        log.info("Generating activities data")
        start = datetime.datetime.now()
        activities : list[model.Activity] = model.generate_activities(self.__dataset, users)
        end = datetime.datetime.now()
        log.info(f"Generated activities in {end - start}")
        log.info("Uploading activities data")
        start = datetime.datetime.now()
        for activity in activities:
            self.__cursor.execute(queries.insert_activity, (activity.id, activity.user_id, activity.transportation_mode, activity.start_date_time, activity.end_date_time))
        self.__db_connection.commit()
        end = datetime.datetime.now()
        log.success(f'Generated {len(activities)} activities in {end - start}')

        # Upload trackpoints
        log.info("Generating trackpoints data")
        start = datetime.datetime.now()
        trackpoints : list[model.Trackpoint] = model.generate_trackpoints(self.__dataset, users)
        end = datetime.datetime.now()
        log.info(f"Generated trackpoints in {end - start} seconds")
        log.info("Uploading trackpoints data")
        start = datetime.datetime.now()
        for (i,trackpoint) in enumerate(trackpoints):
            print(f"{(i+1)/len(trackpoints)}%")
            self.__cursor.execute(queries.insert_new_trackpoint, (trackpoint.activity_id, trackpoint.lat, trackpoint.lon, trackpoint.altitude, trackpoint.date_days, trackpoint.date_time))
        self.__db_connection.commit()
        end = datetime.datetime.now()
        log.success(f'Generated {len(trackpoints)} trackpoints in {end - start}')

    def set_dataset(self, dataset):
        self.__dataset = dataset

    def set_nuke(self, nuke):
        self.__nuke = nuke