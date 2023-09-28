import model as Model
import os
import performance
import config
import db as Database


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
        _ = performance.Timer("(App) App create tables")

        if self.__nuke:
            Database.nuke_database()

        if self.should_reset_db():
            self.reset_db()

        while self.__running:
            self.__running = False

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
