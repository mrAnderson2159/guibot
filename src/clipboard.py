import re
from pyperclip import copy, paste

class Clipboard:
    @staticmethod
    def copy(text: str):
        """Copy text to the clipboard."""
        copy(text)

    @staticmethod
    def paste() -> str:
        """Paste text from the clipboard."""
        return paste()
    
    @classmethod
    def clear(cls):
        """Clear the clipboard."""
        cls.copy("")

    @classmethod
    def contains(cls, text: str, case_sensitive: bool = False) -> bool:
        """
        Check if the clipboard contains the specified text.
        
        :param text: The text to check for in the clipboard.
        :param case_sensitive: If True, the check is case-sensitive; otherwise, it is case-insensitive.
        :return: True if the clipboard contains the text, False otherwise.
        """
        clipboard_text = cls.paste()
        if not case_sensitive:
            text = text.lower()
            clipboard_text = clipboard_text.lower()
        return text in clipboard_text
    
    @classmethod
    def contains_any(cls, keywords: list[str], case_sensitive: bool = False) -> bool:
        """
        Check if the clipboard contains any of the specified keywords.
        
        :param keywords: A list of keywords to check for in the clipboard.
        :param case_sensitive: If True, the check is case-sensitive; otherwise, it is case-insensitive.
        :return: True if any keyword is found in the clipboard, False otherwise.
        """
        for keyword in keywords:
            if cls.contains(keyword, case_sensitive):
                return True
        return False
    
    @classmethod
    def matches(cls, pattern: str | re.Pattern) -> bool:
        """
        Check if the clipboard content matches the specified regex pattern.
        
        :param pattern: A regex pattern or string to match against the clipboard content.
        :return: True if the clipboard content matches the pattern, False otherwise."""
        content = cls.paste()
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        return bool(pattern.search(content))
