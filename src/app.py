import model as Model
import os
import performance
import config
import db as Database
import log
import assignment as Assignment


class App:
    def __init__(self):
        _ = performance.Timer("(App) App init")

        print("NihaoDB v0.0.1-alpha")
        print(config.logo_with_colors)

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
        # every assignment is a method in the Assignment class this runs all of them
        assignment = Assignment.Assignment()
        methods = assignment.methods()
        for method in methods:
            log.log(assignment.format_title(method), "TASK")
            getattr(assignment, method)()

    def should_reset_db(self):
        if self.__nuke:
            return True

        if not Database.tables_exist():
            return True

        if not self.cache_exists():
            return True

        return False

    def reset_db(self):
        Database.create_tables()

        if self.cache_exists():
            data = Model.load_dataset_from_cache(self.__cachefile)
        else:
            data = Model.load_dataset(self.__dataset)

        Model.upload_data(data)

    def set_dataset(self, dataset):
        self.__dataset = dataset

    def set_nuke(self, nuke):
        self.__nuke = nuke

    def cache_exists(self):
        return os.path.exists(self.__cachefile)