from src.mouse_controller import MouseController as mc
from src.keyboard_listener import KeyboardListener as kl
from src.automation import Automation
from src.point import Point
from src.logger import get_logger

logger = get_logger(__name__)

long_wait = 21.5

def power_and_click():
    charge = Point(109, 73)
    download = Point(66, 73)

    mc.click_at(charge)
    mc.click_at(download, 1)
    mc.click_at(charge, long_wait)

def alter_long_wait(offset: float):
    global long_wait
    if long_wait + offset > 0:
        long_wait += offset
        message = f"Long wait time adjusted by {offset} seconds. New long wait time: {long_wait} seconds."
        print(message)
        logger.info(message)
    else:
        message = "Long wait time cannot be negative. No changes made."
        print(message)
        logger.warning(message)

def main():
    print(f"Press 'p' to increase long wait time by 0.5 seconds. Actual value: {long_wait} seconds.")
    print(f"Press 'm' to decrease long wait time by 0.5 seconds. Actual value: {long_wait} seconds.")
    kl.listen_for_key_then('p', alter_long_wait, offset=0.5)
    kl.listen_for_key_then('m', alter_long_wait, offset=-0.5)
    Automation.keystroke("Power and Click", power_and_click, "z")


if __name__ == "__main__":
    main()
