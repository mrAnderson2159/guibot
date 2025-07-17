from src.mouse_controller import MouseController as mc
from src.keyboard_listener import KeyboardListener as kl
from src.automation import Automation
from src.point import Point
from src.logger import get_logger
from collections.abc import Callable
from typing import Literal

logger = get_logger(__name__)

long_wait = 21.5
offset = 0.25

def power_and_click():
    """Automation"""
    charge = Point(109, 73)
    download = Point(66, 73)

    mc.click_at(charge)
    mc.click_at(download, 1)
    mc.click_at(charge, long_wait)

def get_offset(sign: Literal[1, -1]) -> Callable[[], float]:
    def offset_getter() -> float:
        return offset * sign
    return offset_getter

def alter_long_wait(offset_getter: Callable[[], float]):
    global long_wait
    offset = offset_getter()
    if long_wait + offset > 0:
        long_wait += offset
        message = f"Long wait time adjusted by {offset} seconds. New long wait time: {long_wait} seconds."
        print(message)
        logger.info(message)
    else:
        message = "Long wait time cannot be negative. No changes made."
        print(message)
        logger.warning(message)

def alter_offset(multiplier: float):
    global offset
    if multiplier > 0:
        offset *= multiplier
        message = f"Offset adjusted by a factor of {multiplier}. New offset: {offset} seconds."
        print(message)
        logger.info(message)
    else:
        message = "Multiplier must be greater than zero. No changes made."
        print(message)
        logger.warning(message)

def main():
    print(f"Press 'p' to increase long wait time by {offset} seconds. Actual value: {long_wait} seconds.")
    print(f"Press 'm' to decrease long wait time by {offset} seconds. Actual value: {long_wait} seconds.")
    print(f"Press 'd' to double the offset. Actual value: {offset} seconds.")
    print(f"Press 'h' to halve the offset. Actual value: {offset} seconds.")
    kl.listen_for_key_then('p', alter_long_wait, offset_getter=get_offset(1))
    kl.listen_for_key_then('m', alter_long_wait, offset_getter=get_offset(-1))
    kl.listen_for_key_then('d', alter_offset, multiplier=2)
    kl.listen_for_key_then('h', alter_offset, multiplier=0.5)
    Automation.keystroke("Power and Click", power_and_click, "z")


if __name__ == "__main__":
    main()
