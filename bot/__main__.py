"""Telegram bot."""
import logging
import pathlib

import telebot
import telebot.types

import bot.actions
import bot.actions.admin.purchases
import bot.logs
import bot.services
import bot.settings
import bot.storage


bot.logs.setup_logging()

LOGGER = logging.getLogger(__name__)


if __name__ == '__main__':
    LOGGER.info('Starting...')

    user_storage = bot.storage.UserStorage(bot.settings.STORAGE_PATH)
    voting_storage = bot.storage.VotingStorage(bot.settings.STORAGE_PATH)

    codes = [code.strip() for code in open('./ordered.txt')]

    stock_service = bot.services.StockService(
        bot.settings.STOCKS_BASE_URL, codes)
    stocks = stock_service.fetch()

    voting_service = bot.services.VotingManager(voting_storage, user_storage)

    LOGGER.info('Initializing handlers...')

    my_bot = telebot.TeleBot(
        bot.settings.BOT_TOKEN, threaded=False, parse_mode='html')

    user_service = bot.services.UserService(my_bot, user_storage)

    private_messages = bot.actions.PrivateMessage(
        handlers=[
            bot.actions.Welcome(user_storage),
            bot.actions.Voting(voting_service, user_storage, stocks),
            bot.actions.Rules(),
            bot.actions.Menu(),
        ]
    )
    private_messages.as_bot_handler(my_bot)

    admin_group = bot.actions.Group(
        chat_id=bot.settings.BOT_ADMIN_GROUP,
        handlers=[
            bot.actions.Users(user_storage),
            bot.actions.Winners(user_storage),
            bot.actions.StartVoting(user_service, voting_service),
            bot.actions.StopVoting(voting_service),
            bot.actions.admin.purchases.Add(),
        ],        
    )
    admin_group.as_bot_handler(my_bot)

    LOGGER.info('Done. It is up and running.')

    try:
        my_bot.polling()
    except Exception as e:
        LOGGER.exception(str(e))
