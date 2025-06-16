from time import sleep
from typing import Union

from src.enums import Interval
from src.logger import get_logger

logger = get_logger(__name__)

class BaseController:
    @staticmethod
    def wait(time: Union[Interval, float]):
        """
        Wait for a specified interval.

        :param time: Interval to wait.
        """
        if isinstance(time, Interval):
            logger.info(f"Waiting for a {time.name} interval: {time.value} seconds.")
            sleep(time.value)
        elif isinstance(time, (int, float)):
            if time > 0:
                logger.info(f"Waiting for {time} seconds.")
                sleep(time)
            else:
                logger.debug(f"Received non-positive wait time or zero: {time}. No waiting will occur.")
        else:
            message = f"Invalid type for time: {type(time)}. Must be Interval, int, or float."
            logger.error(message)
            raise TypeError(message)
