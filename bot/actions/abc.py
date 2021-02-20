"""Base classes for actions package."""
import abc
import functools
import logging
import threading
import typing

import telebot
import telebot.types


LOGGER = logging.getLogger(__name__)


class BaseHandler(metaclass=abc.ABCMeta):
    """Base handler on telegram actions."""

    @abc.abstractmethod
    def can_handle(self, message: telebot.types.Message) -> bool:
        """Return true if this class can handle action."""

    @abc.abstractmethod
    def handle(self, bot: telebot.TeleBot, message: telebot.types.Message):
        """Do something on action."""


class BaseGroup(metaclass=abc.ABCMeta):
    """Base group of handlers."""

    def __init__(self, handlers: typing.List[BaseHandler]):
        """Primary constructor."""
        self._handlers = handlers
        self._lock = threading.Lock()

    @abc.abstractmethod
    def can_handle(self, message: telebot.types.Message) -> bool:
        """Return true if this group can handle action."""

    def as_bot_handler(self, bot: telebot.TeleBot, *args, **kwargs):
        """Prepare handler and add some extra condition."""

        def can_handle(handler: BaseHandler):
            @functools.wraps(handler)
            def inner(message: telebot.types.Message):
                if not self.can_handle(message):
                    return False
                if not handler.can_handle(message):
                    return False
                return True
            return inner

        def handle(handler: BaseHandler):
            @functools.wraps(handler)
            def inner(message: telebot.types.Message):
                try:
                    return handler.handle(bot, message)
                except Exception as e:
                    LOGGER.exception(str(e))
            return inner

        for handler in self._handlers:
            bot.message_handler(
                func=can_handle(handler),
                content_types=('text', 'document'),
            )(handle(handler))
