import datetime

import config
import log

def print_timer(timer):
    end = datetime.datetime.now()
    duration = end - timer.start

    if duration.total_seconds() < 1:
        duration = duration.total_seconds() * 1000
        log.timer("{} took {:.2f}ms".format(timer.name,duration))
    elif duration.total_seconds() < 60:
        duration = duration.total_seconds()
        log.timer("{} took {:.2f}s".format(timer.name,duration))
    elif duration.total_seconds() < 60 * 60:
        duration = duration.total_seconds() / 60
        log.timer("{} took {:.2f}m".format(timer.name,duration))
    else:
        duration = duration.total_seconds() / 60 / 60
        log.timer("{} took {:.2f}h".format(timer.name,duration))

class Timer:
    def __init__(self, name:str, func=lambda timer: print_timer(timer)) -> None:
        self.name = name
        self.start = datetime.datetime.now()
        self.__func = func

    def __del__(self):
        if config.PERFORMANCE_TESTING:
            self.__func(self)