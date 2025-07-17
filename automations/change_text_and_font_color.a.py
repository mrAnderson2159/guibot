# Automation: change_text_and_font_color
from src.mouse_controller import MouseController as mc
from src.keyboard_controller import KeyboardController as kc
from src.automation import Automation
from src.point import Point
from pynput.keyboard import Key

# WORKS WITH GOOGLE DOCS MENU TAB OPEN
def change_text_and_font_color():
    CHAR_DIMENSION = Point(654, 170)
    FONT_COLOR = Point(813, 170)
    COLOR_BLACK = Point(822, 205)

    mc.click_at(CHAR_DIMENSION)
    mc.double_click()
    kc.delete()
    kc.type("11")
    kc.enter()
    mc.click_at(FONT_COLOR)
    mc.click_at(COLOR_BLACK)


def main():
    Automation.keystroke("change_text_and_font_color", change_text_and_font_color, Key.f3)

if __name__ == "__main__":
    main()
