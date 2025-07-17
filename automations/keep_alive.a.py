# Automation: keep_alive
from src.mouse_controller import MouseController as mc
from src.automation import Automation
from src.point import Point

def keep_alive():
    mc.move_by_offset(50, 0, slowly=True)
    mc.move_by_offset(-50, 0, slowly=True)

def main():
    Automation.loop("keep_alive", keep_alive)

if __name__ == "__main__":
    main()
