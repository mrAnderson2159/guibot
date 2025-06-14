from pynput.keyboard import Key, Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
from src.logger import get_logger

logger = get_logger(__name__)

def esc_exit(key, callback: callable = lambda: None, *args, **kwargs) -> bool:
    if key == Key.esc:
        callback(*args, **kwargs)
        logger.info("Exiting with 'esc' keystroke.")
        return False
    return True

class Automation:
    @staticmethod
    def loop(name: str, automation_function: callable):
        """
        Start a keyboard listener that listens for the 'esc' key to exit the loop.

        :param name: Name of the automation process.
        :param automation_function: Function to be executed in the loop.
        """
        running = True

        def stop_running():
            nonlocal running
            running = False

        def on_press(key):
            return esc_exit(key, stop_running)

        KeyboardListener(on_press=on_press).start()
        logger.info(f"Automation loop started for {name}. Press 'esc' to exit.")
        print(f"Automation loop started for {name}. Press 'esc' to exit.")

        while running:
            try:
                automation_function()
            except KeyboardInterrupt:
                logger.info("Automation loop interrupted by user.")
                print("Automation loop interrupted by user.")
                break


    @staticmethod
    def keystroke(name: str, automation_function: callable, key_activator: str):
        """
        Start a keyboard listener that listens for a specific key activator to trigger the automation function.

        :param name: Name of the automation process.
        :param automation_function: Function to be executed when the key activator is pressed.
        :param key_activator: Single character string that activates the automation function.
        """
        assert isinstance(key_activator, str) and len(key_activator) == 1, "Key activator must be a single character string."

        intro = (f"Starting keystroke automation for '{name}' with activator '{key_activator}'. "
                 f"Press '{key_activator}' to activate the function or 'esc' to exit.")

        logger.info(intro)
        print(intro)

        def on_press(key):
            if hasattr(key, 'char') and key.char == key_activator:
                logger.info(f"Activating automation function '{name}' with keystroke '{key_activator}'.")
                automation_function()
            return esc_exit(key)

        with KeyboardListener(on_press=on_press) as listener:
            listener.join()


    @staticmethod
    def acquire_clicks():
        """
        Start a mouse listener that logs the position of the mouse when clicked.
        """
        def on_click(x, y, button, pressed):
            if pressed:
                point = (x, y)
                logger.info(f"Mouse clicked at {point}.")
                print(f"Mouse clicked at {point}.")

        def on_press(key):
            return esc_exit(key)

        intro = ("Starting mouse listener to acquire points. "
                "Click anywhere to log the mouse position or press 'esc' to exit.")
        logger.info(intro)
        print(intro)

        mouse_listener = MouseListener(on_click=on_click)
        mouse_listener.start()

        keyboard_listener = KeyboardListener(on_press=on_press)
        keyboard_listener.start()

        keyboard_listener.join()
        mouse_listener.stop()
        mouse_listener.join()
