# Automation: resize_image
from src.mouse_controller import MouseController as mc
from src.keyboard_controller import KeyboardController as kc
from src.keyboard_listener import KeyboardListener as kl
from pynput.keyboard import Key
from src.automation import Automation
from src.point import Point

def resize_image(scroll_down: bool = False):
    right_click_position = Point(497, 573)
    option_position = Point(553, 609)
    width_textbox = Point(1353, 343)
    height_textbox = Point(1490, 343)
    close_button = Point(1582, 177)

    # Open context menu on the image
    mc.move_to(right_click_position)
    mc.right_click()

    # Open the resize options
    mc.click_at(option_position)

    # Type the new x dimension
    mc.click_at(width_textbox)
    mc.double_click()
    kc.type("12.15")

    # Type the new y dimension
    mc.click_at(height_textbox)
    mc.double_click()
    kc.type("15.12")

    # Center the image
    kc.hotkey(Key.cmd, Key.shift, 'e')

    # Close resize options
    mc.click_at(close_button)

    # Scroll back to image position
    mc.click_at(right_click_position)
    if scroll_down:
        mc.scroll(0, 75)

def main():
    Automation.keystroke("resize_image", resize_image, Key.f1, blocking=False)
    Automation.keystroke("resize_image_scroll", lambda: resize_image(scroll_down=True), Key.f2)

if __name__ == "__main__":
    main()
