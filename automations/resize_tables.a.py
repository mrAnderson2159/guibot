# Automation: resize_tables
from pynput.keyboard import Key
from src.mouse_controller import MouseController as mc
from src.keyboard_controller import KeyboardController as kc
from src.automation import Automation
from src.point import Point

left_cell = Point(277, 365)
left_cell_tables_options = Point(322, 881)
width = Point(1580, 360)
right_cell = Point(500, 375)
table_layout = Point(1392, 180)
table_centered = Point(1512, 347)
close_table_options = Point(1641, 124)
last_cell = Point(1050, 375)

def resize_two_cols_table():
    # Hide the menu bar
    kc.hotkey(Key.ctrl, Key.shift, 'f')
    mc.wait(0.5)  # Wait for the menu bar to hide

    # Open table options
    mc.move_to(left_cell)
    mc.right_click()
    mc.click_at(left_cell_tables_options)

    # Set left cell width
    mc.move_to(width)
    mc.wait(0.5)  # Wait for the options to appear
    mc.double_click()
    kc.type("5")

    # Select right cell
    mc.click_at(right_cell)

    # Set right cell width
    mc.move_to(width)
    mc.double_click()
    kc.type("20")

    # Center table
    mc.click_at(table_layout)
    mc.click_at(table_centered, 1)

    # close layout options
    mc.click_at(table_layout)

    # # Close table options
    # mc.click_at(close_table_options, 1)

    # Ensure the mouse is back in a sensible position after resizing
    mc.click_at(right_cell)

    # Show the menu bar again
    kc.hotkey(Key.ctrl, Key.shift, 'f')

def resize_three_cols_table():
        # Hide the menu bar
    kc.hotkey(Key.ctrl, Key.shift, 'f')
    mc.wait(0.5)  # Wait for the menu bar to hide

    # Open table options
    mc.move_to(left_cell)
    mc.right_click()
    mc.click_at(left_cell_tables_options)

    # Set left cell width
    mc.move_to(width)
    mc.wait(0.5)  # Wait for the options to appear
    mc.double_click()
    kc.type("5")

    # Select center cell
    mc.click_at(right_cell)

    # Set center cell width
    mc.move_to(width)
    mc.double_click()
    kc.type("15")

    # Select right cell
    mc.click_at(last_cell)

    # Set right cell width
    mc.move_to(width)
    mc.double_click()
    kc.type("5")

        # Center table
    mc.click_at(table_layout)
    mc.click_at(table_centered, 1)

    # close layout options
    mc.click_at(table_layout)

    # # Close table options
    # mc.click_at(close_table_options, 1)

    # Ensure the mouse is back in a sensible position after resizing
    mc.click_at(right_cell)

    # Show the menu bar again
    kc.hotkey(Key.ctrl, Key.shift, 'f')


def main():
    Automation.keystroke("resize_two_cols_table", resize_two_cols_table, Key.f5, blocking=False)
    Automation.keystroke("resize_three_cols_table", resize_three_cols_table, Key.f6)

if __name__ == "__main__":
    main()
