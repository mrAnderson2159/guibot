from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Key
from typing import Union
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
    def keystroke(name: str, automation_function: callable, key_activator: Union[str, Key, list[Union[str, Key]]], blocking: bool = True):
        """
        Start a keyboard listener that listens for a specific key or combination of keys to activate the automation

        :param name: Name of the automation process.
        :param automation_function: Function to be executed when the key is pressed.
        :param key_activator: A single character string, a Key, or a list of strings or Keys that will activate the automation function.
        :param blocking: If True, the listener will block the main thread until it is stopped. If False, it will run in the background
        and allow the main thread to continue executing.
        """
        assert isinstance(key_activator, Key) \
            or isinstance(key_activator, str) and len(key_activator) == 1 \
            or (isinstance(key_activator, list) and all(isinstance(k, (str, Key)) for k in key_activator)), \
            "key_activator must be a single character string, a Key, or a list of strings or Keys."

        listener = None

        if isinstance(key_activator, list):
            key_activator = [(k.name if hasattr(k, 'name') else k.char) if isinstance(k, Key) else k for k in key_activator]
            hotkeys = "+".join(key_activator)

            intro = (f"Starting keystroke automation for '{name}' with hotkeys '{hotkeys}'. "
                     f"Press '{hotkeys}' to activate the function or 'esc' to exit.")
            logger.info(intro)
            print(intro)

            listener = kl.listen_for_hotkeys_then(key_activator, automation_function)
        else:
            key_name = key_activator if isinstance(key_activator, str) else key_activator.name

            intro = (f"Starting keystroke automation for '{name}' with activator '{key_name}'. "
                    f"Press '{key_name}' to activate the function or 'esc' to exit.")
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
