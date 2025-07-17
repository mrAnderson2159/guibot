from typing import Union
from src.base_controller import BaseController
from pynput.keyboard import Key, Controller
from src.enums import Interval
from src.logger import get_logger


logger = get_logger(__name__)
keyboard = Controller()


class KeyboardController(BaseController):
    @classmethod
    def press(cls, key: str, must_wait: bool = True):
        """ Press a key on the keyboard. 
        
        :param key: The key to press, e.g., 'a', 'b', 'c', etc.
        :param must_wait: If True, it will wait for a short interval before pressing the key.
        """
        if must_wait:
            cls.wait(Interval.SHORT)

        logger.info(f"Pressing the '{key}' key.")
        keyboard.press(key)

    @classmethod
    def release(cls, key: str, must_wait: bool = True):
        """ Release a key on the keyboard. 
        
        :param key: The key to release, e.g., 'a', 'b', 'c', etc.
        :param must_wait: If True, it will wait for an instant interval after releasing the key.
        """
        logger.info(f"Releasing the '{key}' key.")
        keyboard.release(key)

        if must_wait:
            cls.wait(Interval.INSTANT)

    @classmethod
    def type(cls, text: str):
        """ Type a string of text. 
        
        :param text: The text to type."""
        cls.wait(Interval.INSTANT)
        logger.info(f"Typing text: {text}")
        keyboard.type(text)

    @classmethod
    def typewrite(cls, text: str, delay: float = Interval.INSTANT):
        """ Type a string of text with a slight delay between each character. 
        
        :param text: The text to type.
        :param delay: The delay in seconds between each character. Default is 0.1 seconds (an instant).
        """
        logger.info(f"Typewriting text: {text}")

        for char in text:
            keyboard.press(char)
            keyboard.release(char)
            cls.wait(delay)


    @classmethod
    def press_key(cls, key: Key, must_wait: bool = True):
        """ Press a special key on the keyboard.

        :param key: The special key to press, e.g., Key.enter, Key.space, etc.
        :param must_wait: If True, it will wait for a short interval before pressing the key.
        """
        if must_wait:
            cls.wait(Interval.SHORT)

        logger.info(f"Pressing the '{key}' key.")
        keyboard.press(key)

    @classmethod
    def release_key(cls, key: Key, must_wait: bool = True):
        """ Release a special key on the keyboard.

        :param key: The special key to release, e.g., Key.enter, Key.space, etc.
        :param must_wait: If True, it will wait for an instant interval after releasing the key.
        """
        logger.info(f"Releasing the '{key}' key.")
        keyboard.release(key)

        if must_wait:
            cls.wait(Interval.INSTANT)

    @classmethod
    def press_and_release(cls, key: str, must_wait: bool = True):
        """ Press and release a key on the keyboard.

        :param key: The key to press and release, e.g., 'a', 'b', 'c', etc.
        :param must_wait: If True, it will wait for a short interval before pressing the key and after releasing it.
        """
        cls.press(key, must_wait)
        cls.release(key, must_wait)

    @classmethod
    def press_and_release_key(cls, key: Key, must_wait: bool = True):
        """ Press and release a special key on the keyboard.

        :param key: The special key to press and release, e.g., Key.enter, Key.space, etc.
        :param must_wait: If True, it will wait for a short interval before pressing the key and after releasing it.
        """
        cls.press_key(key, must_wait)
        cls.release_key(key, must_wait)

    @classmethod
    def enter(cls, must_wait: bool = True):
        """ Press and release the Enter key.

        :param must_wait: If True, it will wait for a short interval before pressing the key.
        """
        cls.press_key(Key.enter, must_wait)
        cls.release_key(Key.enter, must_wait)

    @classmethod
    def delete(cls, must_wait: bool = True):
        """ Press and release the Delete key.

        :param must_wait: If True, it will wait for a short interval before pressing the key.
        """
        cls.press_key(Key.delete, must_wait)
        cls.release_key(Key.delete, must_wait)

    @classmethod
    def space(cls, must_wait: bool = True):
        """ Press and release the Space key.

        :param must_wait: If True, it will wait for a short interval before pressing the key.
        """
        cls.press_key(Key.space, must_wait)
        cls.release_key(Key.space, must_wait)

    @classmethod
    def escape(cls, must_wait: bool = True):
        """ Press and release the Escape key.

        :param must_wait: If True, it will wait for a short interval before pressing the key.
        """
        cls.press_key(Key.esc, must_wait)
        cls.release_key(Key.esc, must_wait)

    @classmethod
    def tab(cls, must_wait: bool = True):
        """ Press and release the Tab key.

        :param must_wait: If True, it will wait for a short interval before pressing the key.
        """
        cls.press_key(Key.tab, must_wait)
        cls.release_key(Key.tab, must_wait)

    @classmethod
    def hotkey(cls, *keys: Union[Key, str], wait: Union[Interval, float] = Interval.INSTANT):
        for key in keys:
            keyboard.press(key)

        cls.wait(wait)

        for key in reversed(keys):
            keyboard.release(key)
