__all__ = ['get_logger']

import logging
from colored import Fore, Style
from src.env import get_logging_level

# Get the logging level from the environment variable
logging_level = getattr(logging, get_logging_level().upper(), None)
if logging_level is not None and not isinstance(logging_level, int):
    raise ValueError(f"Invalid logging level: {get_logging_level()}")


# Configure the logging settings
if isinstance(logging_level, int):
    format = (f'{Fore.cyan}%(asctime)s {Style.reset}- '
              f'{Fore.magenta}%(name)s {{%(lineno)s}} {Style.reset}- '
              f'{Fore.green}%(levelname)s {Style.reset}- '
              f'{Fore.yellow}%(message)s{Style.reset}')

    print(f"Logging level set to: {logging_level}")

    logging.basicConfig(
        level=logging_level,
        format=format,
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.

    :param name: Name of the logger.
    :return: Configured logger instance.
    """
    return logging.getLogger(name)
