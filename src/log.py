
colors = {
    "ERROR": "\033[1;31m",
    "SUCCESS": "\033[1;32m",
    "WARNING": "\033[1;33m",
    "INFO": "\033[1;34m",
    "TIMER": "\033[1;30m",
}

def log(msg: str, color: str = None):
    if color:
        print(f"{colors[color]}[{color}]\033[0m {msg}")
    else:
        print(msg)

def error(msg: str):
    log(msg, "ERROR")

def success(msg: str):
    log(msg, "SUCCESS")

def warning(msg: str):
    log(msg, "WARNING")

def info(msg: str):
    log(msg, "INFO")

def timer(msg: str):
    log(msg, "TIMER")