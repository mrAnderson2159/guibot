from src.mouse_controller import MouseController as mc
from src.automation import Automation
from src.point import Point

def power_and_click():
    charge = Point(109, 73)
    download = Point(66, 73)

    mc.click_at(charge)
    mc.click_at(download, 1)
    mc.click_at(charge, 21.5)

def main():
    Automation.keystroke("Power and Click", power_and_click, "z")


if __name__ == "__main__":
    main()
