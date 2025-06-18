from typing import Union
from pynput.keyboard import Key, Listener
from src.logger import get_logger

logger = get_logger(__name__)

class KeyboardListener:
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
            logger.info("Exiting with 'esc' keystroke.")
            return False
        return True

    @classmethod
    def listen_for_key_then(cls, key: Union[str, Key], callback: callable, *args, **kwargs):
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
        print(message)
        logger.info(message)

        Listener(on_press=on_press).start()

if __name__ == "__main__":
    # Example for listening to a specific key
    def specific_key_callback():
        print("Specific key pressed!")

    KeyboardListener.listen_for_key_then('a', specific_key_callback)
    KeyboardListener.listen_for_key_then('b', specific_key_callback)

    while True:
        try:
            pass  # Keep the main thread alive
        except KeyboardInterrupt:
            print("Exiting...")
            break
