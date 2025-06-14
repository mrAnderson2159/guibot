from os import getenv

def get_logging_level() -> str:
    """
    Get the logging level from the environment variable 'LOG'.
    If the variable is not set, it defaults to 'NONE'.
    :return: Logging level as a string.
    """
    return getenv("LOG", "NONE")
