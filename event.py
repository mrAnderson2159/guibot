from typing import *
import asyncio
from asyncio.locks import Event as AsyncEvent


def event_creator(func):
    def wrapper(cls, event_name, *args, **kwargs):
        if event_name not in cls.events:
            cls.events[event_name] = AsyncEvent()
        return func(cls, event_name, *args, **kwargs)
    return wrapper


class Event:
    events: dict[str, AsyncEvent] = {}

    @classmethod
    @event_creator
    def emit(cls, event_name: str, *args, **kwargs):
        pass

    @classmethod
    @event_creator
    def on(cls, event_name: str, callback: callable, *args, **kwargs):
        pass
