"""DI configuration for services."""
import json
import typing

import injector
import pydantic
import telebot

import bot.entities
import bot.services
import bot.storage


class ServiceModule(injector.Module):
    """DI module for services."""

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
                binder.injector.get(bot.storage.QuotesStorage),
            ))
        binder.multibind(
            typing.List[bot.entities.Stock], lambda: pydantic.parse_obj_as(
                typing.List[bot.entities.Stock],
                json.load(open('./stocks.json')),
            ))
