"""DI configuration for services."""
import typing

import telebot
import injector

import bot.entities
import bot.services
import bot.storage


class ServiceModule(injector.Module):
    """DI module for services."""

    def __init__(self, codes: typing.List[str]):
        """Primary constructor."""
        self._codes = codes

    def configure(self, binder: injector.Binder):
        """Configure services."""
        binder.bind(
            bot.services.VotingManager, lambda: bot.services.VotingManager(
                binder.injector.get(bot.storage.VotingStorage),
                binder.injector.get(bot.storage.UserStorage),
            ))
        binder.bind(
            bot.services.UserService, lambda: bot.services.UserService(
                binder.injector.get(telebot.TeleBot),
                binder.injector.get(bot.storage.UserStorage),
            ))
        binder.bind(
            bot.services.StockService, lambda: bot.services.StockService(
                bot.settings.STOCKS_BASE_URL,
                self._codes,
            ))
        binder.multibind(
            typing.List[bot.entities.Stock], lambda: binder.injector.get(
                bot.services.StockService,
            ).fetch())
