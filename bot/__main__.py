"""Telegram bot."""
import logging

import click
import injector
import telebot

import bot.actions
import bot.actions.admin.ask_for_vote
import bot.actions.admin.dump
import bot.actions.admin.purchases
import bot.actions.admin.results
import bot.logs
import bot.modules
import bot.services
import bot.services.modules
import bot.settings
import bot.storage
import bot.cron.history


bot.logs.setup_logging()

LOGGER = logging.getLogger('bot')


def get_container():
    """Prepare and return base DI container."""
    codes = [code.strip() for code in open('./ordered.txt')]

    container = injector.Injector(modules=[
        bot.modules.MainModule(),
        bot.modules.StorageModule(),
        bot.services.modules.ServiceModule(codes),
    ])

    return container


@click.group()
def cli():
    """Nothing to do."""


@cli.command()
def polling():
    """Start polling."""
    LOGGER.info('Starting bot...')
    container = get_container()

    private_messages = bot.actions.PrivateMessage(
        handlers=[
            container.get(bot.actions.Welcome),
            container.get(bot.actions.Voting),
            container.get(bot.actions.Rules),
            container.get(bot.actions.Menu),
        ],
    )

    admin_group = bot.actions.Group(
        chat_id=bot.settings.BOT_ADMIN_GROUP,
        handlers=[
            container.get(bot.actions.Users),
            container.get(bot.actions.Winners),
            container.get(bot.actions.StartVoting),
            container.get(bot.actions.StopVoting),
            container.get(bot.actions.admin.purchases.Add),
            container.get(bot.actions.admin.purchases.List),
            container.get(bot.actions.admin.results.Results),
            container.get(bot.actions.admin.ask_for_vote.AskForVote),
            container.get(bot.actions.admin.dump.Dump),
        ],
    )

    my_bot = container.get(telebot.TeleBot)

    admin_group.as_bot_handler(my_bot)
    private_messages.as_bot_handler(my_bot)

    LOGGER.info('Done. It is up and running.')

    try:
        my_bot.polling()
    except Exception as e:
        LOGGER.exception(str(e))


@cli.group()
def cron():
    """Blank group for cron jobs."""


@cron.command()
def fetch():
    """Fetch historical prices."""
    container = get_container()

    bot.cron.history.fetch(
        container.get(bot.storage.PurchaseStorage),
        '123'
    )


if __name__ == '__main__':
    cli()
