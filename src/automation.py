from pynput.mouse import Listener as MouseListener
from threading import Thread
from src.keyboard_listener import KeyboardListener as kl
from src.logger import get_logger

logger = get_logger(__name__)


class Automation:
    @staticmethod
    def loop(name: str, automation_function: callable, blocking: bool = True):
        """
        Start a keyboard listener that listens for the 'esc' key to exit the loop.

        :param name: Name of the automation process.
        :param automation_function: Function to be executed in the loop.
        """
        running = True

        def stop_running():
            nonlocal running
            running = False

        message = (f"Starting automation loop for '{name}'. "
                   "Press 'esc' to stop the automation loop.")
        print(message)
        logger.info(message)
        kl.exit_on_esc(stop_running)

        def thread_body():
            """
            This function runs in a separate thread to allow the main thread to continue executing.
            It will run the automation function repeatedly until the 'esc' key is pressed.
            """
            while running:
                try:
                    automation_function()
                except KeyboardInterrupt:
                    message = f"Automation {name} interrupted by user."
                    print(message)
                    logger.info(message)
                    break

        thread = Thread(target=thread_body)
        thread.start()

        if blocking:
            thread.join()


    @staticmethod
    def keystroke(name: str, automation_function: callable, key_activator: str, blocking: bool = True):
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

        listener = kl.listen_for_key_then(key_activator, automation_function)

        if blocking:
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

        intro = ("Starting mouse listener to acquire points. "
                "Click anywhere to log the mouse position or press 'esc' to exit.")
        logger.info(intro)
        print(intro)

        ml = MouseListener(on_click=on_click)
        ml.start()

        kl.exit_on_esc().join()
        ml.stop()
        ml.join()
