from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Key
from typing import Union
from threading import Thread
from enum import Enum
from src.keyboard_listener import KeyboardListener as kl
from src.logger import get_logger

logger = get_logger(__name__)

def _is_allowed(condition: callable, error_message: str):
    def decorator(func):
        def wrapper(cls, *args, **kwargs):
            if condition(cls):
                return func(cls, *args, **kwargs)
            else:
                logger.error(error_message)
                raise RuntimeError(error_message)
        return wrapper
    return decorator


class AutomationMode(Enum):
    NONE = ''
    LOOP = 'loop'
    KEYSTROKE = 'keystroke'
    CLICK = 'click'

class Automation:
    """
    Manages the start and control of automations.

    This class provides methods to execute automation functions in the following modes:
    - continuous (loop)
    - reactive to key presses (keystroke / hotkey)
    - interactive (mouse click acquisition)

    It is designed to ensure consistency and safety during execution, preventing conflicts between different types of automation
    and monitoring the number of active threads.

    Private attributes:
    -------------------
    - __att : AutomationMode
        Active Thread Type. Identifies the type of automation currently running ('loop', 'keystroke', etc.).
        Used to block the simultaneous start of incompatible types of automation.

    - __aptc : int
        Active Parallel Thread Count. Tracks the number of currently active automations.

    - __pl : int
        Parallel Limit (default: 10). Limits the maximum number of simultaneous keystroke-type automations.
        Ignored when a loop-mode automation is active.
    """
    __att: AutomationMode = AutomationMode.NONE
    __aptc: int = 0
    __pl: int = 10

    @classmethod
    def get_active_thread_type(cls) -> str:
        """Get the type of the currently active automation thread."""
        return cls.__att

    @classmethod
    def get_active_parallel_thread_count(cls) -> int:
        """Get the count of currently active parallel automation threads."""
        return cls.__aptc

    @classmethod
    def get_parallel_limit(cls) -> int:
        """Get the maximum number of parallel automations allowed."""
        return cls.__pl

    @classmethod
    def set_parallel_limit(cls, value: int):
        """Set the maximum number of parallel automations allowed."""
        if value < 1:
            raise ValueError("Parallel limit must be at least 1.")
        cls.__pl = value

    @classmethod
    @_is_allowed(lambda cls: cls.get_active_thread_type() == AutomationMode.NONE,
                  "Cannot start a loop automation while another is running.")
    def loop(cls, name: str, automation_function: callable):
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
                    cls.__att = AutomationMode.NONE
                    cls.__aptc -= 1
                    logger.debug(f"Active thread type set to {cls.__att}. Active parallel thread count: {cls.__aptc}.")
                    break

        thread = Thread(target=thread_body)
        thread.start()

        cls.__att = AutomationMode.LOOP
        cls.__aptc += 1
        logger.debug(f"Active thread type set to {cls.__att}. Active parallel thread count: {cls.__aptc}.")

        thread.join()

    @classmethod
    @_is_allowed(lambda cls: cls.get_active_thread_type() != AutomationMode.LOOP,
                  "Cannot start a keystroke automation while a loop automation is running.")
    def keystroke(cls, name: str, automation_function: callable, key_activator: Union[str, Key, list[Union[str, Key]]], blocking: bool = True):
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

        cls.__att = AutomationMode.KEYSTROKE
        cls.__aptc += 1
        logger.debug(f"Active thread type set to {cls.__att}. Active parallel thread count: {cls.__aptc}.")

        def cleanup():
            listener.join()
            if cls.__att == AutomationMode.KEYSTROKE:
                cls.__aptc -= 1
                if cls.__aptc == 0:
                    cls.__att = AutomationMode.NONE
            logger.debug(f"Name: {name}. Active thread type set to {cls.__att}. Active parallel thread count: {cls.__aptc}.")

        if blocking:
            cleanup()
        else:
            Thread(target=cleanup, daemon=True).start()


    @classmethod
    @_is_allowed(lambda cls: True, "It's always allowed.")
    def acquire_clicks(cls):
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

        cls.__att = AutomationMode.CLICK
        cls.__aptc += 1
        logger.debug(f"Active thread type set to {cls.__att}. Active parallel thread count: {cls.__aptc}.")

        kl.exit_on_esc().join()
        ml.stop()
        ml.join()

        if cls.get_active_thread_type() == AutomationMode.CLICK:
            cls.__att = AutomationMode.NONE
        cls.__aptc -= 1
        logger.debug(f"Active thread type set to {cls.__att}. Active parallel thread count: {cls.__aptc}.")
