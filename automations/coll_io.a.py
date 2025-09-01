# Automation: coll_io
from pynput.keyboard import Key
from pynput.mouse import Listener as ml
from src.mouse_controller import MouseController as mc
from src.keyboard_controller import KeyboardController as kc
from src.keyboard_listener import KeyboardListener as kl
from src.clipboard import Clipboard as cb
from src.automation import Automation
from src.point import Point
from time import sleep


global_points: dict[str, Point] = {
    "psoc": Point(80, 80),
    "serial_terminal": Point(1100, 100),
}

def set_points():
    performed_clicks = 0
    points_to_set = ["psoc", "serial_terminal"]

    def on_click(x, y, _, pressed):
        nonlocal performed_clicks
        if pressed:
            if performed_clicks < len(points_to_set):
                point_name = points_to_set[performed_clicks]
                global_points[point_name] = Point(x, y)
                print(f"Point '{point_name}' set at ({x}, {y})")
                performed_clicks += 1
            if performed_clicks >= len(points_to_set):
                print("All points set. Exiting listener.")
                return False
        return True

    # Sleep for listener threads synchronization
    sleep(.3)
    with ml(on_click=on_click) as listener:
        print("Click to set points for: " + ", ".join(points_to_set))
        listener.join()


def program_psoc():
    start = global_points["psoc"]
    if start is None:
        print("Error: 'psoc' point not set. Please set the points first.")
        return
    mc.click_at(start)

def enter_utech():
    serial_terminal = global_points["serial_terminal"]
    mc.click_at(serial_terminal)
    mc.wait(0.5)
    kc.typewrite("UTECH")
    kc.enter()
    mc.click_at(serial_terminal + Point(0, 100))

def main():
    # You can add multiple automations with different keys by using the keyword argument blocking=False
    # for every automation but the last one.z
    Automation.keystroke("set_points", set_points, 's', blocking=False)
    Automation.keystroke("program_psoc", program_psoc, 'z', blocking=False)
    Automation.keystroke("enter_utech", enter_utech, 'x')

if __name__ == "__main__":
    main()
