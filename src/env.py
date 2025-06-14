from os import getenv

def get_logging_level() -> str:
    return getenv("LOG", "NONE")
