import model as Model
import os
import performance
import config
import db as Database
import log
import tabulate


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

        # 3
        log.log("Task 2.3", "TASK")
        top_15_users_activities = Database.get_top_users_most_activites(15)
        log.info("Top 15 users with most activities:")
        print(tabulate.tabulate(top_15_users_activities, headers=["User ID", "Number of activities"]))

        # 4
        log.log("Task 2.4", "TASK")
        users_that_have_taken_the_bus = Database.get_all_users_that_used("bus")
        log.info("Users that have taken the bus:")
        print(tabulate.tabulate(users_that_have_taken_the_bus, headers=["User ID"]))

        # 5
        log.log("Task 2.5", "TASK")
        top_10_users_with_the_most_different_transportation_modes = Database.get_top_users_with_the_most_different_transportation_modes(10)
        log.info("Top 10 users with the most different transportation modes:")
        print(tabulate.tabulate(top_10_users_with_the_most_different_transportation_modes, headers=["User ID", "Number of different transportation modes"]))

        # 6
        log.log("Task 2.6", "TASK")
        duplicate_activities = Database.get_all_duplicate_activities()
        log.info("Duplicate activities:")
        print(tabulate.tabulate(duplicate_activities, headers=["User ID", "Activity ID", "Start date time", "End date time"]))

        # 7
        log.log("Task 2.7.a", "TASK")
        users_with_activities_lasting_to_next_day = Database.get_amount_of_users_with_activities_lasting_to_next_day()
        log.info(f"Amount of users with activities lasting to the next day: {users_with_activities_lasting_to_next_day}")

        log.log("Task 2.7.b", "TASK")
        user_transportation_mode_activities = Database.get_user_transportation_activity_hours_lasting_to_next_day(limit=True)
        log.info("Users with activities lasting to the next day (limit=15):")
        print(tabulate.tabulate(user_transportation_mode_activities, headers=["User ID", "Transportation mode", "duration (hours)"]))
        

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