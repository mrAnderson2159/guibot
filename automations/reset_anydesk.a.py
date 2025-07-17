# Automation: reset_anydesk
from pynput.keyboard import Key
from src.mouse_controller import MouseController as mc
from src.automation import Automation
from src.point import Point

def reset_anydesk():
    terminal = Point(655, 960)
    mouse_position = mc.get_position()

    mc.move_to(terminal)
    mc.double_click()
    mc.move_to(mouse_position)

def main():
    Automation.keystroke("reset_anydesk", reset_anydesk, '|')

if __name__ == "__main__":
    main()
