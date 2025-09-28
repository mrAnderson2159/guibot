# Automation: bridge
from pynput.keyboard import Key
from src.mouse_controller import MouseController as mc
from src.keyboard_controller import KeyboardController as kc
from src.keyboard_listener import KeyboardListener as kl
from src.clipboard import Clipboard as cb
from src.automation import Automation
from src.point import Point

left_bridge = Point(100, 100)
central_bridge = Point(700, 150)
right_bridge = Point(1595, 265)
bottom = Point(1066, 1066)
power = None # TODO: Add the Point(x, y) of PSoC power button here


def bridge(entry_point: Point):
    mc.click_at(bottom)
    mc.click_at(entry_point)
    kc.typewrite("\r")
    kc.typewrite("root")
    kc.wait(.5)
    kc.enter(must_wait=False)
    kc.wait(.5)
    kc.typewrite("******") # TODO: insert the root password here
    kc.enter(must_wait=False)
    kc.wait(7)
    kc.typewrite("flash-nand")
    kc.enter(must_wait=False)
    mc.click_at(bottom)

def poweroff():
    kc.enter()
    kc.wait(1)
    kc.typewrite("poweroff")
    kc.enter(must_wait=False)
    mc.click_at(bottom)

def start_programming_PSoC():
    # TODO: First update the power Point above
    mc.click_at(power)
    mc.click_at(bottom)

def main():
    # You can add multiple automations with different keys by using the keyword argument blocking=False
    # for every automation but the last one.
    Automation.keystroke("type poweroff", poweroff, Key.f1, blocking=False)
    Automation.keystroke("left bridge", lambda: bridge(left_bridge), Key.f10, blocking=False)
    Automation.keystroke("central bridge", lambda: bridge(central_bridge), Key.f11, blocking=False)
    Automation.keystroke("right bridge", lambda: bridge(right_bridge), Key.f12, blocking=False)
    Automation.keystroke("program bridge", start_programming_PSoC, 'z')


if __name__ == "__main__":
    main()
