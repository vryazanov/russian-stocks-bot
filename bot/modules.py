"""For DI modules."""
import injector
import telebot

import bot.settings
import bot.storage


class MainModule(injector.Module):
    """Main di module."""

    def configure(self, binder: injector.Binder):
        """Configure main classes."""
        binder.bind(telebot.TeleBot, lambda: telebot.TeleBot(
            token=bot.settings.BOT_TOKEN,
            threaded=False,
            parse_mode='html',
        ))


class StorageModule(injector.Module):
    """DI module for storages."""

    def configure(self, binder: injector.Binder):
        """Configure storages."""
        binder.bind(
            bot.storage.UserStorage, lambda: bot.storage.UserStorage(
                bot.settings.STORAGE_PATH,
            ))
        binder.bind(
            bot.storage.VotingStorage, lambda: bot.storage.VotingStorage(
                bot.settings.STORAGE_PATH,
            ))
        binder.bind(
            bot.storage.PurchaseStorage, lambda: bot.storage.PurchaseStorage(
                bot.settings.STORAGE_PATH,
            ))
        binder.bind(
            bot.storage.QuotesStorage, lambda: bot.storage.QuotesStorage(
                bot.settings.STORAGE_PATH,
            ))
