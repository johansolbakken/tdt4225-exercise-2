import model as Model
import os
import performance
import config
import db as Database
import log


class App:
    def __init__(self):
        _ = performance.Timer("(App) App init")

        print("NihaoDB v0.0.1-alpha")
        print(config.logo_with_colors)

        self.__running: bool = True
        self.__nuke: bool = False
        self.__dataset: str = ""
        self.__cachefile: str = ".appcache/memcache.pkl"

        Database.init()

    def __del__(self):
        _ = performance.Timer("(App) App shutdown")
        Database.shutdown()

    def run(self):
        # -------------- Part 1 --------------
        log.log("Task 1", "TASK")

        if self.__nuke:
            _ = performance.Timer("(App) App nuke database")
            Database.nuke_database()

        if self.should_reset_db():
            _ = performance.Timer("(App) App reset database")
            self.reset_db()

        # -------------- Part 2 --------------

        # 1
        log.log("Task 2.1", "TASK")
        number_of_users = Database.get_number_of_users()
        log.info(f"Number of users: {number_of_users}")

        number_of_activities = Database.get_number_of_activities()
        log.info(f"Number of activities: {number_of_activities}")

        number_of_trackpoints = Database.get_number_of_trackpoints()
        log.info(f"Number of trackpoints: {number_of_trackpoints}")

        # 2
        log.log("Task 2.2", "TASK")
        average_trackpoints_per_user = Database.get_average_trackpoints_per_user()
        log.info(f"Average trackpoints per user: {average_trackpoints_per_user}")

        max_trackpoints_per_user = Database.get_max_trackpoints_per_user()
        log.info(f"Max trackpoints per user: {max_trackpoints_per_user}")

        min_trackpoints_per_user = Database.get_min_trackpoints_per_user()
        log.info(f"Min trackpoints per user: {min_trackpoints_per_user}")

    
    def should_reset_db(self):
        if self.__nuke:
            return True

        if not Database.tables_exist():
            return True

        if not self.cache_exists():
            return True

        return False

    def reset_db(self):
        Database.nuke_database()
        Database.create_tables()

        if self.cache_exists():
            data = Model.load_dataset_from_cache(self.__cachefile)
        else:
            data = Model.load_dataset(self.__dataset)

        Database.upload_data(data)

    def set_dataset(self, dataset):
        self.__dataset = dataset

    def set_nuke(self, nuke):
        self.__nuke = nuke

    def cache_exists(self):
        return os.path.exists(self.__cachefile)
