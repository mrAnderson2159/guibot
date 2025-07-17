from typing import Union
from pynput.keyboard import Key, Listener
from src.logger import get_logger
from time import sleep


logger = get_logger(__name__)

class KeyboardListener:
    @staticmethod
    def safe_start_listener(*args, **kwargs) -> Listener:
        """ Start a keyboard listener with a slight delay to ensure safe synchronization of AXIsProcessTrusted.
        This is useful to avoid issues with the listener starting before the system is ready.

        :param args: Positional arguments to pass to the Listener.
        :param kwargs: Keyword arguments to pass to the Listener.
        :return: An instance of Listener that has been started.
        """
        syncro_time = 0.1  # seconds
        logger.info(f"Starting listener with a synchronization delay of {syncro_time} seconds.")
        sleep(syncro_time) # allow safe synchronization of AXIsProcessTrusted
        listener = Listener(*args, **kwargs)
        listener.start()
        return listener

    @staticmethod
    def check_for_esc(key: Union[str, Key], callback: callable = lambda: None, *args, **kwargs) -> bool:
        """
        Check if the pressed key is 'esc' and call the callback function if it is.

        :param key: The key that was pressed.
        :param callback: Function to call when 'esc' is pressed.
        :param args: Additional arguments to pass to the callback function.
        :param kwargs: Additional keyword arguments to pass to the callback function.
        :return: True if the key is not 'esc', False otherwise.
        If False is returned, the listener will stop. Else, it will continue listening.
        """
        if key == Key.esc:
            callback(*args, **kwargs)
            message = "Exiting listener due to 'esc' keystroke."
            logger.info(message)
            return False
        return True

    @classmethod
    def exit_on_esc(cls, callback: callable = lambda: None, *args, **kwargs) -> Listener:
        """
        Start a keyboard listener that exits when 'esc' is pressed and calls the callback function.

        Note that this method will not block the main thread, allowing other operations to continue.

        :param callback: Function to call when 'esc' is pressed.
        :param args: Additional arguments to pass to the callback function.
        :param kwargs: Additional keyword arguments to pass to the callback function.
        """
        def on_press(key: Union[str, Key]):
            return cls.check_for_esc(key, callback, *args, **kwargs)

        return cls.safe_start_listener(on_press=on_press)

    @classmethod
    def listen_for_key_then(cls, key: Union[str, Key], callback: callable, *args, **kwargs) -> Listener:
        """
        Start a keyboard listener that listens for a specific key to trigger the callback function.
        Use 'esc' to exit the listener.

        Note that this method will not block the main thread, allowing other operations to continue.

        :param key: The key to listen for.
        :param callback: Function to call when the specified key is pressed.
        :param args: Additional arguments to pass to the callback function.
        :param kwargs: Additional keyword arguments to pass to the callback function.
        """
        def on_press(pressed_key: Union[str, Key]):
            """
            Callback function that is called when a key is pressed.
            It checks if the pressed key matches the specified key and calls the callback function if it does.
            It also checks for the 'esc' key to stop the listener.

            :param pressed_key: The key that was pressed.
            :return: True if the listener should continue, False if it should stop.
            """
            if isinstance(key, str):
                try:
                    if pressed_key.char == key:
                        callback(*args, **kwargs)
                except AttributeError:
                    pass  # non è un tasto con `.char`, ignora
            elif isinstance(key, Key):
                if pressed_key == key:
                    callback(*args, **kwargs)
            else:
                logger.error(f"Unsupported key type: {type(key)}. Expected str or Key.")
                raise TypeError(f"Unsupported key type: {type(key)}. Expected str or Key.")

            return cls.check_for_esc(pressed_key)
        
        message = f"Listening for key: {key}. Press it to trigger the callback. Press 'esc' to stop listening."
        logger.info(message)

        return cls.safe_start_listener(on_press=on_press)


    @classmethod
    def listen_for_hotkeys_then(cls, keys: list[Union[str, Key]], callback: callable, *args, **kwargs) -> Listener:
        """
        Listen for a specific hotkey (combination of keys) and trigger callback when all are pressed together.
        """
        def normalize(key: Union[str, Key]) -> str:
            if isinstance(key, str):
                return key
            else:
                return key.name if hasattr(key, 'name') else key.char

        expected = set(map(normalize, keys))
        pressed = set()

        def on_press(pressed_key):
            if not cls.check_for_esc(pressed_key):
                return False

            try:
                pressed.add(normalize(pressed_key))
            except AttributeError:
                pass  # Ignore keys without .name or .char

            if pressed == expected:
                callback(*args, **kwargs)

            return True

        def on_release(released_key):
            try:
                pressed.discard(normalize(released_key))
            except AttributeError:
                pass

        log_keys = " + ".join(expected)
        logger.info(f"Listening for hotkey: {log_keys}. Press all to trigger callback. Press 'esc' to stop.")

        return cls.safe_start_listener(on_press=on_press, on_release=on_release)


def __blocking_loop():
    while True:
        try:
            pass  # Keep the main thread alive
        except KeyboardInterrupt:
            print("Exiting...")
            break


__test = 'hotkeys'  # Change to 'multithreading' to test multithreading functionality


if __name__ == "__main__" and __test == 'multithreading':
    # Example for listening to a specific key
    def specific_key_callback():
        print("Specific key pressed!")

    KeyboardListener.listen_for_key_then('a', specific_key_callback)
    KeyboardListener.listen_for_key_then('b', specific_key_callback)

    __blocking_loop()

if __name__ == "__main__" and __test == 'hotkeys':
    # Example for listening to a hotkey
    def hotkey_callback():
        print("cmd + ctrl + 1 pressed!")

    KeyboardListener.listen_for_hotkeys_then([Key.cmd, Key.ctrl, '1'], hotkey_callback)

    __blocking_loop()
